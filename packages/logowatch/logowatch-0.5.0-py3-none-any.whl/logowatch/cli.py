"""
Command-line interface for logowatch.

Provides a user-friendly CLI with rich colored output for log analysis.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from logowatch import __version__
from logowatch.analyzer import LogAnalyzer
from logowatch.config import (
    Config,
    load_config,
    load_legacy_config,
    convert_legacy_to_yaml,
    discover_config,
    CONFIG_FILE_NAMES,
)
from logowatch.models import AnalysisResult, RuleResult, Severity
from logowatch.presets import list_presets, get_preset_content


LOG_FORMAT_RECOMMENDATIONS = """
# Log Format Recommendations for Logowatch

## Tier 1: Optimal (Best for multi-source aggregation)
**JSON/JSONL with ISO 8601 timestamp:**
```json
{"timestamp": "2026-01-14T09:15:32.123Z", "level": "INFO", "message": "..."}
```
- ✓ Easy timestamp extraction (field path)
- ✓ Structured data for filtering
- ✓ No regex needed

## Tier 2: Good (Structured text with standard timestamp)
**ISO 8601 prefix:**
```
2026-01-14T09:15:32.123Z INFO [service] Message here
```
- ✓ Standard timestamp format
- ✓ Auto-detectable
- Pattern: `^(?P<ts>\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})`

## Tier 3: Acceptable (Common log formats)
**Common Log Format (nginx/apache):**
```
192.168.1.1 - - [14/Jan/2026:09:15:32 +0000] "GET /api" 200
```
- Pattern: `\\[(?P<ts>\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2}[^\\]]*)\\]`
- Format: `%d/%b/%Y:%H:%M:%S %z`

**Syslog format:**
```
Jan 14 09:15:32 hostname service[pid]: Message
```
- Pattern: `^(?P<ts>\\w{3}\\s+\\d{1,2}\\s+\\d{2}:\\d{2}:\\d{2})`
- Format: `%b %d %H:%M:%S` (note: no year - uses current year)

## Tier 4: Avoid (Hard to parse)
- Custom date formats without separators: `20260114091532`
- Ambiguous formats: `01/14/26` (MM/DD/YY vs DD/MM/YY)
- No timestamp at all

## Example Configuration

```yaml
sources:
  - name: api
    path: /var/log/api.log
    timestamp:
      field: "timestamp"  # For JSON logs

  - name: nginx
    path: /var/log/nginx/access.log
    timestamp:
      pattern: '\\[(?P<ts>[^\\]]+)\\]'
      format: "%d/%b/%Y:%H:%M:%S %z"

  - name: syslog
    path: /var/log/syslog
    timestamp:
      auto: true  # Auto-detect common formats

output:
  mode: sequential
  sort_by: timestamp
```
"""

console = Console()


def _get_available_presets() -> list[str]:
    """Get list of available preset names."""
    return list(list_presets().keys())


def severity_style(severity: Severity) -> str:
    """Get Rich style for severity level."""
    styles = {
        Severity.ERROR: "bold red",
        Severity.WARNING: "bold yellow",
        Severity.INFO: "bold cyan",
    }
    return styles.get(severity, "white")


def severity_icon(severity: Severity) -> str:
    """Get icon for severity level."""
    icons = {
        Severity.ERROR: "[red]✗[/red]",
        Severity.WARNING: "[yellow]⚠[/yellow]",
        Severity.INFO: "[cyan]ℹ[/cyan]",
    }
    return icons.get(severity, "•")


def print_header() -> None:
    """Print the application header."""
    console.print()
    console.print(
        Panel(
            "[bold blue]LOGOWATCH[/bold blue] - Autonomous Log Analysis",
            subtitle=f"v{__version__}",
            box=box.DOUBLE,
        )
    )
    console.print()


def print_summary(result: AnalysisResult) -> None:
    """Print analysis summary."""
    table = Table(title="Analysis Summary", box=box.ROUNDED)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Sources", ", ".join(result.sources_analyzed))
    table.add_row("Total Lines", f"{result.total_lines:,}")
    table.add_row("[red]Errors[/red]", f"[red]{result.total_errors:,}[/red]")
    table.add_row("[yellow]Warnings[/yellow]", f"[yellow]{result.total_warnings:,}[/yellow]")
    table.add_row("[cyan]Info[/cyan]", f"[cyan]{result.total_info:,}[/cyan]")

    if result.incremental:
        mode_text = "[green]INCREMENTAL[/green] (new errors only)"
    else:
        mode_text = "[dim]FULL[/dim] (all errors)"
    table.add_row("Mode", mode_text)

    if result.last_check:
        table.add_row("Last Check", result.last_check.strftime("%Y-%m-%d %H:%M:%S"))

    console.print(table)
    console.print()


def print_rule_result(rule_result: RuleResult, max_examples: int = 5, truncate: int = 140) -> None:
    """Print results for a single rule."""
    rule = rule_result.rule
    icon = severity_icon(rule.severity)
    style = severity_style(rule.severity)

    # Header - indicate JSON format if used
    format_tag = f" [dim](jsonl)[/dim]" if rule.format in ("json", "jsonl") else ""
    console.print(f"{icon} [{style}]{rule.description}[/{style}]{format_tag}: {rule_result.total_count}")

    # Show examples (0 = unlimited)
    from rich.markup import escape
    examples = rule_result.matches if max_examples == 0 else rule_result.matches[:max_examples]
    for match in examples:
        # Use formatted_content if available (from JSON parsing), otherwise raw content
        display_content = match.formatted_content or match.content
        if truncate > 0:
            display_content = display_content[:truncate]
        console.print(f"   [dim]│[/dim] [dim]L{match.line_number}:[/dim] {escape(display_content)}")

        # Show context before
        for ctx_line in match.context_before:
            console.print(f"   [dim]│  {escape(ctx_line[:100])}[/dim]")

        # Show extracted values ONLY if no display template (avoid duplication)
        if not match.formatted_content:
            for name, value in match.extracted_values.items():
                console.print(f"   [dim]├─[/dim] [green]{name}:[/green] {escape(str(value))}")

        # Show context after
        for ctx_line in match.context_after:
            console.print(f"   [dim]│  {escape(ctx_line[:100])}[/dim]")

    # Show remaining count (only if limited)
    if max_examples > 0:
        remaining = rule_result.total_count - min(len(rule_result.matches), max_examples)
        if remaining > 0:
            console.print(f"   [dim]│[/dim] [cyan]... and {remaining} more[/cyan]")

    # Show aggregations
    if rule_result.aggregations:
        console.print(f"   [dim]├─[/dim] [bold]Distribution:[/bold]")
        for value, count in list(rule_result.aggregations.items())[:10]:
            console.print(f"   [dim]│[/dim]   {escape(str(value))}: {count}")

    # Show related patterns
    if rule_result.related_patterns:
        console.print(f"   [dim]├─[/dim] [bold]Related:[/bold]")
        for related in rule_result.related_patterns[:5]:
            console.print(f"   [dim]│[/dim]   {escape(related[:80])}")

    console.print()


def print_results(result: AnalysisResult, max_examples: int = 5, truncate: int = 140) -> None:
    """Print all results grouped by section or severity."""
    from collections import defaultdict

    # Group results by section
    by_section: dict[str | None, list[RuleResult]] = defaultdict(list)
    for rule_result in result.rule_results:
        section = rule_result.rule.section
        by_section[section].append(rule_result)

    # Print custom sections first (sorted alphabetically)
    custom_sections = sorted([s for s in by_section.keys() if s is not None])
    for section in custom_sections:
        section_results = by_section[section]
        if section_results:
            # Determine section color based on highest severity in section
            max_severity = max(r.rule.severity for r in section_results)
            color = {"error": "red", "warning": "yellow", "info": "cyan"}.get(
                max_severity.value, "white"
            )
            console.print(f"[bold {color}]─── {section.upper()} ───[/bold {color}]")
            console.print()
            for rule_result in section_results:
                print_rule_result(rule_result, max_examples, truncate)

    # Print rules without custom section, grouped by severity
    no_section = by_section.get(None, [])
    if no_section:
        # Group by severity
        by_severity: dict[Severity, list[RuleResult]] = defaultdict(list)
        for rule_result in no_section:
            by_severity[rule_result.rule.severity].append(rule_result)

        # Print in severity order: ERROR, WARNING, INFO
        severity_config = [
            (Severity.ERROR, "red", "ERRORS"),
            (Severity.WARNING, "yellow", "WARNINGS"),
            (Severity.INFO, "cyan", "INFO"),
        ]

        for severity, color, label in severity_config:
            severity_results = by_severity.get(severity, [])
            if severity_results:
                console.print(f"[bold {color}]─── {label} ───[/bold {color}]")
                console.print()
                for rule_result in severity_results:
                    print_rule_result(rule_result, max_examples, truncate)


def print_final_status(result: AnalysisResult) -> None:
    """Print final status message."""
    if result.total_errors == 0:
        console.print(
            Panel(
                "[bold green]✓ No critical errors found![/bold green]",
                box=box.ROUNDED,
            )
        )
    elif result.total_errors <= 10:
        console.print(
            Panel(
                f"[bold yellow]⚠ Found {result.total_errors} errors - review recommended[/bold yellow]",
                box=box.ROUNDED,
            )
        )
    else:
        console.print(
            Panel(
                f"[bold red]✗ Found {result.total_errors} errors - urgent attention needed![/bold red]",
                box=box.ROUNDED,
            )
        )


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Logowatch - Autonomous log analysis with configurable pattern rules."""
    pass


@main.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option(
    "--limit", "-l",
    default=5,
    help="Max examples per rule (default: 5)",
)
@click.option(
    "--no-incremental",
    is_flag=True,
    help="Disable incremental mode (show all errors)",
)
@click.option(
    "--source", "-s",
    multiple=True,
    help="Analyze specific source(s) only",
)
@click.option(
    "--json", "output_json",
    is_flag=True,
    help="Output as JSON instead of rich text",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output to file (plain text without colors)",
)
@click.option(
    "--full", "-f",
    is_flag=True,
    help="Show full content without truncation",
)
@click.option(
    "--sequential", "-S",
    is_flag=True,
    help="Output in line order (chronological) instead of grouped by rule",
)
@click.option(
    "--cache-path", "-c",
    type=click.Path(),
    help="Custom path for cache file",
)
def analyze(
    config_path: str,
    limit: int,
    no_incremental: bool,
    source: tuple[str, ...],
    output_json: bool,
    output: Optional[str],
    full: bool,
    sequential: bool,
    cache_path: Optional[str],
) -> None:
    """Analyze logs using configuration file."""
    config = load_config(config_path)
    cache = Path(cache_path) if cache_path else None
    truncate = 0 if full else config.output.truncate  # 0 = no truncation, default 500 chars
    # CLI flag overrides config; default to config setting
    output_mode = "sequential" if sequential else config.output.mode

    analyzer = LogAnalyzer(
        config,
        cache_path=cache,
        incremental=not no_incremental,
    )

    sources = list(source) if source else None
    result = analyzer.analyze(source_names=sources, max_examples=limit)

    if output_json:
        import json
        json_output = json.dumps(result.model_dump(mode="json"), indent=2, default=str)
        if output:
            Path(output).write_text(json_output)
            console.print(f"[green]✓[/green] JSON output written to: {output}")
        else:
            click.echo(json_output)
    elif output:
        # Write plain text to file
        from io import StringIO
        buffer = StringIO()
        file_console = Console(file=buffer, force_terminal=False, width=200)
        source_files = [str(Path(s.path).resolve()) for s in config.sources]
        _print_report(file_console, result, limit, show_summary=True, truncate=truncate, mode=output_mode, sort_by=config.output.sort_by, source_files=source_files)
        Path(output).write_text(buffer.getvalue())
        console.print(f"[green]✓[/green] Report written to: {output}")
    else:
        print_header()
        print_summary(result)
        print_results(result, max_examples=limit, truncate=truncate)
        print_final_status(result)


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--pattern", "-p",
    multiple=True,
    help="Pattern(s) to search for",
)
@click.option(
    "--limit", "-l",
    default=None,
    type=int,
    help="Max matches to show (0 = unlimited, default: from config or 0)",
)
@click.option(
    "--config", "-c",
    type=click.Path(),
    help="Config file path (priority: --config > --preset > auto-discover)",
)
@click.option(
    "--preset", "-P",
    type=click.Choice(_get_available_presets(), case_sensitive=False),
    help="Use preset (mcp, claude-session, docker)",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output to file",
)
@click.option(
    "--full", "-f",
    is_flag=True,
    help="Show full content without truncation",
)
@click.option(
    "--sequential", "-S",
    is_flag=True,
    help="Output in line order (chronological)",
)
@click.option(
    "--no-incremental",
    is_flag=True,
    default=True,
    help="Show all matches (default for scan)",
)
def scan(
    file_path: str,
    pattern: tuple[str, ...],
    limit: int,
    config: Optional[str],
    preset: Optional[str],
    output: Optional[str],
    full: bool,
    sequential: bool,
    no_incremental: bool,
) -> None:
    """Scan a log file with patterns, preset, or config.

    This is the PRIMARY command. Priority: --config > --preset > auto-discover.

    Examples:
        logowatch scan session.jsonl --preset claude-session -o chat.txt
        logowatch scan app.log -c myconfig.yaml
        logowatch scan server.log -p ERROR -p WARN
    """
    from logowatch.models import Rule, LogSource

    config_obj: Config | None = None
    config_path: Path | None = None
    preset_name: str | None = None
    source_file = str(Path(file_path).resolve())

    # Priority: --config > --preset > auto-discover
    if config:
        config_path = Path(config)
        config_obj = load_config(config_path)
        console.print(f"[green]Config:[/green] {config_path}")
    elif preset:
        # Use preset - create temp config with preset rules
        preset_content = get_preset_content(preset)
        if not preset_content:
            console.print(f"[red]Error:[/red] Preset '{preset}' not found")
            raise SystemExit(1)
        preset_name = preset
        # Parse preset and override source path, keep original source name for rule matching
        import yaml
        preset_data = yaml.safe_load(preset_content)
        orig_source_name = preset_data['sources'][0]['name'] if preset_data.get('sources') else 'scan'
        preset_data['sources'] = [{'name': orig_source_name, 'path': file_path, 'type': 'file'}]
        config_obj = Config.model_validate(preset_data)
        console.print(f"[green]Preset:[/green] {preset}")
    else:
        # Auto-discover config near the log file
        config_path = discover_config(start_path=file_path, walk_up=True)
        if config_path:
            config_obj = load_config(config_path)
            console.print(f"[dim]Auto-discovered:[/dim] {config_path}")

    # Determine rules to use
    if pattern:
        rules = [
            Rule(pattern=p, description=f"Pattern: {p}", severity=Severity.INFO)
            for p in pattern
        ]
        if config_obj is None:
            config_obj = Config(rules=rules)
        else:
            config_obj = config_obj.model_copy(update={'rules': rules})
    elif config_obj and config_obj.rules:
        rules = config_obj.rules
    else:
        rules = [
            Rule(pattern=r"ERROR", description="Errors", severity=Severity.ERROR),
            Rule(pattern=r"WARNING", description="Warnings", severity=Severity.WARNING),
            Rule(pattern=r"Exception|Traceback", description="Exceptions", severity=Severity.ERROR),
        ]
        config_obj = Config(rules=rules)

    # Override source to the specified file (only if not already set by preset)
    if not preset:
        source_name = config_obj.sources[0].name if config_obj.sources else 'scan'
        config_obj = config_obj.model_copy(update={
            'sources': [LogSource(name=source_name, path=Path(file_path), type='file')]
        })

    truncate = 0 if full else config_obj.output.truncate
    output_mode = "sequential" if sequential else config_obj.output.mode
    # Use CLI limit if provided, otherwise config's max_examples (0 = unlimited)
    max_examples = limit if limit is not None else config_obj.output.max_examples
    analyzer = LogAnalyzer(config_obj, incremental=False)
    result = analyzer.analyze(max_examples=max_examples)

    # Output
    if output:
        from io import StringIO
        buffer = StringIO()
        file_console = Console(file=buffer, force_terminal=False, width=200)
        _print_report(file_console, result, max_examples, show_summary=True, truncate=truncate, mode=output_mode, sort_by=config_obj.output.sort_by, source_files=[source_file], preset_name=preset_name)
        Path(output).write_text(buffer.getvalue())
        console.print(f"[green]✓[/green] Output: {output}")
    else:
        print_header()
        print_summary(result)
        print_results(result, max_examples=max_examples, truncate=truncate)


@main.command()
@click.option(
    "--limit", "-l",
    default=None,
    type=int,
    help="Max examples per rule (overrides config)",
)
@click.option(
    "--no-incremental",
    is_flag=True,
    help="Disable incremental mode (overrides config)",
)
@click.option(
    "--incremental/--all",
    default=None,
    help="Incremental or all errors (overrides config)",
)
@click.option(
    "--json", "output_json",
    is_flag=True,
    help="Output as JSON (overrides config)",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output to file (overrides config)",
)
@click.option(
    "--full", "-f",
    is_flag=True,
    help="Show full content without truncation",
)
@click.option(
    "--sequential", "-S",
    is_flag=True,
    help="Output in line order (chronological) instead of grouped by rule",
)
@click.option(
    "--walk-up", "-w",
    is_flag=True,
    help="Search parent directories for config (default: only current dir)",
)
def run(
    limit: Optional[int],
    no_incremental: bool,
    incremental: Optional[bool],
    output_json: bool,
    output: Optional[str],
    full: bool,
    sequential: bool,
    walk_up: bool,
) -> None:
    """Run analysis with auto-discovered config.

    Searches for .logowatch.yaml in CURRENT DIRECTORY only by default.
    Use --walk-up to also search parent directories.
    """
    cwd = Path.cwd()
    config_path = discover_config(walk_up=walk_up)

    if not config_path:
        console.print(f"[red]Error:[/red] No config file found in {cwd}")
        console.print(f"[dim]Searched for:[/dim] {', '.join(CONFIG_FILE_NAMES)}")
        console.print()
        console.print("Options:")
        console.print("  1. Create config: [bold]logowatch init[/bold]")
        console.print("  2. Use explicit path: [bold]logowatch analyze <config.yaml>[/bold]")
        if not walk_up:
            console.print("  3. Search parent dirs: [bold]logowatch run --walk-up[/bold]")
        raise SystemExit(1)

    # Show absolute path for clarity
    abs_config = config_path.resolve()
    if abs_config.parent == cwd:
        console.print(f"[green]Config:[/green] {config_path.name} [dim](current directory)[/dim]")
    else:
        console.print(f"[yellow]Config:[/yellow] {abs_config} [dim](from parent directory)[/dim]")

    config = load_config(config_path)

    # Determine incremental mode (CLI overrides config)
    use_incremental = config.incremental  # Default from config
    if no_incremental:
        use_incremental = False
    elif incremental is not None:
        use_incremental = incremental

    # Determine output format (CLI overrides config)
    output_format = config.output.format
    if output_json:
        output_format = "json"
    elif output:
        output_format = "file"

    # Determine max examples (CLI overrides config)
    max_examples = limit if limit is not None else config.output.max_examples

    # Determine output file (CLI overrides config)
    output_file = Path(output) if output else config.output.file_path

    # Determine truncation and output mode
    truncate = 0 if full else config.output.truncate
    output_mode = "sequential" if sequential else config.output.mode

    cache_dir = config.cache_dir or config_path.parent
    cache_file = cache_dir / ".logowatch_cache.json"

    analyzer = LogAnalyzer(
        config,
        cache_path=cache_file,
        incremental=use_incremental,
    )

    result = analyzer.analyze(max_examples=max_examples)

    # Output based on format
    if output_format == "json":
        import json
        json_output = json.dumps(result.model_dump(mode="json"), indent=2, default=str)
        if output_file:
            output_file.write_text(json_output)
            console.print(f"[green]✓[/green] JSON output written to: {output_file}")
        else:
            click.echo(json_output)
    elif output_format == "file" and output_file:
        # Write plain text report to file
        from io import StringIO
        buffer = StringIO()
        file_console = Console(file=buffer, force_terminal=False, width=200)
        source_files = [str(Path(s.path).resolve()) for s in config.sources]
        _print_report(file_console, result, max_examples, config.output.show_summary, truncate=truncate, mode=output_mode, sort_by=config.output.sort_by, source_files=source_files)
        output_file.write_text(buffer.getvalue())
        console.print(f"[green]✓[/green] Report written to: {output_file}")
    else:
        # Console output (default)
        print_header()
        if config.output.show_summary:
            print_summary(result)
        print_results(result, max_examples=max_examples, truncate=truncate)
        print_final_status(result)


def _print_report(
    target_console: Console,
    result: AnalysisResult,
    max_examples: int,
    show_summary: bool,
    truncate: int = 500,
    mode: str = "aggregate",
    sort_by: str = "line_number",
    source_files: list[str] | None = None,
    preset_name: str | None = None,
) -> None:
    """Print report to a specific console (for file output)."""
    target_console.print("LOGOWATCH ANALYSIS REPORT")
    target_console.print("=" * 60)

    # Show source file(s) absolute path
    if source_files:
        for sf in source_files:
            target_console.print(f"File: {sf}")
    if preset_name:
        target_console.print(f"Preset: {preset_name}")
    target_console.print()

    if show_summary:
        target_console.print(f"Sources: {', '.join(result.sources_analyzed)}")
        target_console.print(f"Total Lines: {result.total_lines:,}")
        target_console.print(f"Errors: {result.total_errors}")
        target_console.print(f"Warnings: {result.total_warnings}")
        target_console.print(f"Info: {result.total_info}")
        if result.incremental and result.last_check:
            target_console.print(f"Mode: INCREMENTAL (since {result.last_check.strftime('%Y-%m-%d %H:%M')})")
        else:
            target_console.print(f"Mode: {'INCREMENTAL' if result.incremental else 'FULL'}")
        target_console.print()

    if mode == "sequential":
        # Collect all matches with their rule info
        all_matches = []
        for rule_result in result.rule_results:
            examples = rule_result.matches if max_examples == 0 else rule_result.matches[:max_examples]
            for match in examples:
                all_matches.append((match, rule_result.rule))

        # Sort by timestamp or line number
        if sort_by == "timestamp":
            # Sort by parsed_timestamp, None values go to end
            from datetime import datetime
            all_matches.sort(key=lambda x: (
                x[0].parsed_timestamp is None,  # None values last
                x[0].parsed_timestamp or datetime.max,
            ))
        else:
            all_matches.sort(key=lambda x: x[0].line_number)

        # Output in sequence
        multi_source = len(result.sources_analyzed) > 1
        for match, rule in all_matches:
            display_content = match.formatted_content or match.content
            if truncate > 0:
                display_content = display_content[:truncate]
            # Include source name if multiple sources
            source_prefix = f"[{match.source_name}] " if multi_source else ""
            marker = f"[L{match.line_number}] {source_prefix}"
            for line in display_content.split('\n'):
                target_console.print(f"{marker} {line}")
    else:
        # Aggregate mode - group by rule (original behavior)
        for rule_result in result.rule_results:
            rule = rule_result.rule
            icon = {"error": "[ERROR]", "warning": "[WARN]", "info": "[INFO]"}.get(
                rule.severity.value, "[?]"
            )
            format_tag = " (jsonl)" if rule.format in ("json", "jsonl") else ""
            target_console.print(f"{icon} {rule.description}{format_tag}: {rule_result.total_count}")
            examples = rule_result.matches if max_examples == 0 else rule_result.matches[:max_examples]
            for match in examples:
                display_content = match.formatted_content or match.content
                if truncate > 0:
                    display_content = display_content[:truncate]
                marker = f"[L{match.line_number}]"
                for line in display_content.split('\n'):
                    target_console.print(f"{marker} {line}")
            if max_examples > 0 and rule_result.total_count > max_examples:
                target_console.print(f"  ... and {rule_result.total_count - max_examples} more")
            target_console.print()


@main.command()
@click.argument("rules_path", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output YAML file path",
)
def convert(
    rules_path: str,
    output: Optional[str],
) -> None:
    """Convert legacy pipe-delimited config to YAML."""
    yaml_content = convert_legacy_to_yaml(rules_path, output_path=output)

    if output:
        console.print(f"[green]✓[/green] Converted to: {output}")
    else:
        console.print(yaml_content)


@main.command()
@click.argument("config_path", type=click.Path(), required=False)
def validate(config_path: Optional[str]) -> None:
    """Validate configuration file syntax and rules.

    If no config path provided, auto-discovers config file in CURRENT DIRECTORY.
    """
    import re

    # Find config
    if config_path:
        path = Path(config_path)
        if not path.exists():
            console.print(f"[red]Error:[/red] Config file not found: {config_path}")
            raise SystemExit(1)
    else:
        path = discover_config()
        if not path:
            cwd = Path.cwd()
            console.print(f"[red]Error:[/red] No config file found in {cwd}")
            console.print(f"[dim]Searched for:[/dim] {', '.join(CONFIG_FILE_NAMES)}")
            console.print()
            console.print("Specify path: [bold]logowatch validate <config.yaml>[/bold]")
            raise SystemExit(1)

    console.print(f"[green]Validating:[/green] {path.resolve()}")
    console.print()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        config = load_config(path)
    except Exception as e:
        console.print(f"[red]✗ YAML Parse Error:[/red]")
        console.print(f"  {e}")
        raise SystemExit(1)

    # Validate sources
    console.print("[bold]Sources:[/bold]")
    for source in config.sources:
        source_path = Path(source.path)
        if source_path.exists():
            console.print(f"  [green]✓[/green] {source.name}: {source.path}")
        else:
            console.print(f"  [yellow]⚠[/yellow] {source.name}: {source.path} [dim](not found)[/dim]")
            warnings.append(f"Source '{source.name}' path not found: {source.path}")

    console.print()

    # Validate rules
    console.print("[bold]Rules:[/bold]")
    source_names = {s.name for s in config.sources}
    sections_used: set[str] = set()

    for i, rule in enumerate(config.rules):
        rule_id = rule.id or f"rule_{i+1}"

        # Check pattern is valid regex
        try:
            re.compile(rule.pattern)
            pattern_ok = True
        except re.error as e:
            pattern_ok = False
            errors.append(f"Rule '{rule_id}': Invalid regex pattern: {e}")

        # Check source exists
        if rule.source not in source_names and rule.source != "default":
            errors.append(f"Rule '{rule_id}': Source '{rule.source}' not defined")
            source_ok = False
        else:
            source_ok = True

        # Track sections
        if rule.section:
            sections_used.add(rule.section)

        # Check extract/aggregate patterns
        if rule.options:
            if rule.options.extract:
                try:
                    re.compile(rule.options.extract.pattern)
                except re.error as e:
                    errors.append(f"Rule '{rule_id}': Invalid extract pattern: {e}")
            if rule.options.aggregate:
                try:
                    re.compile(rule.options.aggregate.by)
                except re.error as e:
                    errors.append(f"Rule '{rule_id}': Invalid aggregate pattern: {e}")

        # Print rule status
        status = "[green]✓[/green]" if (pattern_ok and source_ok) else "[red]✗[/red]"
        section_info = f" [dim][{rule.section}][/dim]" if rule.section else ""
        console.print(f"  {status} {rule.description}{section_info}")

    console.print()

    # Print sections summary
    if sections_used:
        console.print(f"[bold]Sections:[/bold] {', '.join(sorted(sections_used))}")
        console.print()

    # Print summary
    if errors:
        console.print("[bold red]Errors:[/bold red]")
        for err in errors:
            console.print(f"  [red]✗[/red] {err}")
        console.print()

    if warnings:
        console.print("[bold yellow]Warnings:[/bold yellow]")
        for warn in warnings:
            console.print(f"  [yellow]⚠[/yellow] {warn}")
        console.print()

    # Final verdict
    if errors:
        console.print("[red]✗ Configuration has errors[/red]")
        raise SystemExit(1)
    elif warnings:
        console.print("[yellow]⚠ Configuration valid with warnings[/yellow]")
    else:
        console.print("[green]✓ Configuration is valid[/green]")


@main.command()
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output file path (default: .logowatch.yaml)",
)
@click.option(
    "--log-path", "-l",
    type=click.Path(),
    help="Path to log file/dir to pre-configure in sources",
)
@click.option(
    "--preset", "-p",
    type=click.Choice(_get_available_presets(), case_sensitive=False),
    help="Use a preset template (mcp, claude-session, docker)",
)
@click.option(
    "--list-presets", "list_presets_flag",
    is_flag=True,
    help="List available presets",
)
@click.option(
    "--show-formats",
    is_flag=True,
    help="Show recommended log format documentation",
)
def init(output: Optional[str], log_path: Optional[str], preset: Optional[str], list_presets_flag: bool, show_formats: bool) -> None:
    """Create a .logowatch.yaml configuration file.

    Creates a config file that will be auto-discovered by `logowatch run` and `logowatch scan`.

    Examples:

        logowatch init                           # Basic config
        logowatch init --preset mcp              # For Claude MCP logs
        logowatch init --preset docker -l /var/lib/docker/containers
        logowatch init --list-presets            # Show available presets
        logowatch init --show-formats            # Show log format recommendations
    """
    # Show format recommendations
    if show_formats:
        console.print(LOG_FORMAT_RECOMMENDATIONS)
        return

    # List presets
    if list_presets_flag:
        available_presets = list_presets()
        console.print("[bold]Available Presets:[/bold]")
        console.print()
        for name, info in available_presets.items():
            console.print(f"  [cyan]{name}[/cyan] - {info['name']}")
            console.print(f"      {info['description']}")
            console.print()
        return

    # Determine log path for the template
    if log_path:
        log_path_str = str(Path(log_path).resolve())
        log_name = Path(log_path).stem or "app"
        source_type = "directory" if Path(log_path).is_dir() else "file"
    else:
        log_path_str = "/var/log/app.log"
        log_name = "app"
        source_type = "file"

    # Use preset if specified - copy actual YAML file
    if preset:
        available_presets = list_presets()
        preset_info = available_presets[preset]
        sample_config = get_preset_content(preset)
        if not sample_config:
            console.print(f"[red]Error:[/red] Preset '{preset}' not found")
            raise SystemExit(1)

        # If user provided --log-path, substitute in the preset
        if log_path:
            import re
            # Replace source path and type in the preset YAML
            sample_config = re.sub(
                r'(path:\s*)[^\n]+',
                f'\\1{log_path_str}',
                sample_config,
                count=1  # Only first source
            )
            sample_config = re.sub(
                r'(type:\s*)(file|directory|glob)',
                f'\\1{source_type}',
                sample_config,
                count=1
            )
        console.print(f"[dim]Using preset:[/dim] {preset_info['name']}")
    else:
        sample_config = f"""# LOGOWATCH CONFIG - Log pattern analyzer
# Run: logowatch run | logowatch validate | logowatch run --help
# Docs: https://github.com/lifeaitools/logowatch

# ═══════════════════════════════════════════════════════════════════════════════
# SOURCES - Log files to analyze
# ═══════════════════════════════════════════════════════════════════════════════
# REQUIRED: name, path, type
# type: "file" | "directory" | "glob"
# pattern: glob filter for directory/glob types (default: "*.log")

sources:
  - name: {log_name}
    path: {log_path_str}
    type: file

# ═══════════════════════════════════════════════════════════════════════════════
# RULES - Patterns to detect
# ═══════════════════════════════════════════════════════════════════════════════
# REQUIRED: pattern, description, severity, source
# severity: error | warning | info
# format: text (default) | jsonl (for JSON logs)
# section: custom grouping header (optional, e.g. "Performance", "Security")
#
# OPTIONS (all optional):
#   case_insensitive: true
#   options.context.before: N (lines before match)
#   options.context.after: N (lines after match)
#   options.extract.pattern: "regex with (capture)"
#   options.extract.name: "field_name"
#   options.aggregate.by: "regex with (capture)" or ".field" for JSON
#   options.json.fields: [list, of, keys] - extract these JSON keys
#   options.json.filter: '.level == "ERROR"' - jq-style filter
#   options.json.display: '{timestamp} [{level}] {msg}' - display format

rules:
  # Standard severity-based grouping (no section = grouped by severity)
  - pattern: "ERROR|CRITICAL|FATAL"
    description: "Application errors"
    severity: error
    source: {log_name}
    options:
      context:
        after: 5

  - pattern: "Exception|Traceback"
    description: "Exceptions"
    severity: error
    source: {log_name}
    options:
      context:
        after: 15

  - pattern: "WARN|WARNING"
    description: "Warnings"
    severity: warning
    source: {log_name}

  # Custom section example - rules with same 'section' grouped together
  # - pattern: "query.*(\\\\d+)\\\\s*ms"
  #   description: "Slow queries"
  #   severity: warning
  #   section: "Performance"
  #   source: {log_name}
  #   options:
  #     extract:
  #       pattern: "(\\\\d+)\\\\s*ms"
  #       name: "duration_ms"

  # JSONL logs example - parse JSON and extract fields
  # - pattern: "."
  #   format: jsonl
  #   description: "JSON errors"
  #   severity: error
  #   source: {log_name}
  #   options:
  #     json:
  #       fields: [timestamp, level, message]
  #       filter: '.level == "ERROR"'
  #       display: '{{timestamp}} [{{level}}] {{message}}'
  #     aggregate:
  #       by: ".level"

# ═══════════════════════════════════════════════════════════════════════════════
# OPTIONS
# ═══════════════════════════════════════════════════════════════════════════════

incremental: true      # true = only new errors since last run
cache_dir: null        # null = same as config dir
cache_timeout_hours: 24

# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT OPTIONS
# ═══════════════════════════════════════════════════════════════════════════

output:
  # Format: console (colored), json, or file
  format: console

  # Output file path (used when format: file or format: json with file)
  # file_path: /path/to/report.txt

  # Max examples to show per rule
  max_examples: 5

  # Show summary table at the top
  show_summary: true
"""

    output_path = Path(output) if output else Path(".logowatch.yaml")
    if output_path.exists():
        if not click.confirm(f"{output_path} exists. Overwrite?"):
            return

    output_path.write_text(sample_config)
    console.print(f"[green]✓[/green] Created: {output_path}")
    console.print()
    console.print("[dim]Config file names (auto-discovered):[/dim]")
    for name in CONFIG_FILE_NAMES:
        marker = "[green]✓[/green]" if name == output_path.name else " "
        console.print(f"  {marker} {name}")
    console.print()
    console.print("Edit the file to configure your log sources and rules.")
    console.print("Then run: [bold]logowatch run[/bold] or [bold]logowatch scan <logfile>[/bold]")


if __name__ == "__main__":
    main()

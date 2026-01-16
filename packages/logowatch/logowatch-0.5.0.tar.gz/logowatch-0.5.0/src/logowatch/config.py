"""
Configuration loading and parsing for logowatch.

Supports YAML configuration files with the following structure:

```yaml
sources:
  - name: app
    path: /var/log/app.log
    type: file

  - name: errors
    path: /var/log/errors/
    type: directory
    pattern: "*.log"

rules:
  - pattern: "ERROR.*Connection"
    description: "Connection errors"
    severity: error
    source: app
    options:
      context:
        after: 3
      extract:
        pattern: "host=([\\w.]+)"
        name: "host"
```
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from logowatch.models import LogSource, Rule, RuleOptions


# Config file names to search for (in order of priority)
CONFIG_FILE_NAMES = [
    ".logowatch.yaml",
    ".logowatch.yml",
    ".logowatch",
    "logowatch.yaml",
    "logowatch.yml",
]


class OutputConfig(BaseModel):
    """Output configuration."""

    format: str = Field(
        default="console",
        pattern="^(console|json|file)$",
        description="Output format: console (rich), json, or file",
    )
    mode: str = Field(
        default="aggregate",
        pattern="^(aggregate|sequential)$",
        description="Output mode: aggregate (group by rule) or sequential (by line order)",
    )
    sort_by: str = Field(
        default="line_number",
        pattern="^(line_number|timestamp)$",
        description="Sort mode for sequential output: 'line_number' (default) or 'timestamp'",
    )
    file_path: Path | None = Field(
        default=None,
        description="Output file path (required if format=file)",
    )
    max_examples: int = Field(
        default=0,
        ge=0,
        description="Max examples per rule (0 = unlimited)",
    )
    show_summary: bool = Field(default=True, description="Show summary table")
    show_sources: bool = Field(default=True, description="Show analyzed sources")
    truncate: int = Field(
        default=0,
        ge=0,
        description="Truncate content to N chars (0 = no truncation)",
    )


class Config(BaseModel):
    """Main configuration model."""

    sources: list[LogSource] = Field(default_factory=list)
    rules: list[Rule] = Field(default_factory=list)
    defaults: dict[str, Any] = Field(default_factory=dict)
    cache_dir: Path | None = Field(default=None)
    cache_timeout_hours: int = Field(default=24)

    # Analysis options
    incremental: bool = Field(
        default=True,
        description="Only show new errors since last check",
    )

    # Output options
    output: OutputConfig = Field(default_factory=OutputConfig)

    def get_source(self, name: str) -> LogSource | None:
        """Get source by name."""
        for source in self.sources:
            if source.name == name:
                return source
        return None

    def get_rules_for_source(self, source_name: str) -> list[Rule]:
        """Get all rules for a specific source."""
        return [r for r in self.rules if r.source == source_name and r.enabled]

    def get_rules_by_tag(self, tag: str) -> list[Rule]:
        """Get all rules with a specific tag."""
        return [r for r in self.rules if tag in r.tags and r.enabled]


def discover_config(
    start_path: Path | str | None = None,
    walk_up: bool = False,  # Changed default: don't walk up (more predictable for agents)
    check_home: bool = False,  # Changed default: don't check home (more predictable)
) -> Path | None:
    """
    Discover a config file by searching standard locations.

    Search order:
    1. Directory of start_path (if provided)
    2. Parent directories (if walk_up=True) - disabled by default for predictability
    3. Current working directory
    4. User home directory (if check_home=True) - disabled by default

    Args:
        start_path: Starting file or directory to search from
        walk_up: Whether to walk up parent directories (default: False for predictability)
        check_home: Whether to check ~/.logowatch.yaml (default: False)

    Returns:
        Path to config file if found, None otherwise
    """
    searched: list[Path] = []

    # Start from the given path
    if start_path:
        start_path = Path(start_path).resolve()
        if start_path.is_file():
            start_path = start_path.parent
        searched.append(start_path)

        # Walk up parent directories
        if walk_up:
            parent = start_path.parent
            while parent != parent.parent:  # Stop at root
                searched.append(parent)
                parent = parent.parent

    # Add current directory
    cwd = Path.cwd()
    if cwd not in searched:
        searched.append(cwd)

    # Add home directory
    if check_home:
        home = Path.home()
        if home not in searched:
            searched.append(home)

    # Search for config files
    for directory in searched:
        for config_name in CONFIG_FILE_NAMES:
            config_path = directory / config_name
            if config_path.exists() and config_path.is_file():
                return config_path

    return None


def load_config(path: Path | str | None = None, auto_discover: bool = False) -> Config:
    """
    Load configuration from YAML file.

    Args:
        path: Path to config file (if None and auto_discover=True, will search)
        auto_discover: If True and path is None, search for config file

    Returns:
        Config object

    Raises:
        FileNotFoundError: If config file not found
    """
    if path is None:
        if auto_discover:
            discovered = discover_config()
            if discovered:
                path = discovered
            else:
                raise FileNotFoundError(
                    f"No config file found. Searched for: {', '.join(CONFIG_FILE_NAMES)}"
                )
        else:
            raise ValueError("Either path must be provided or auto_discover=True")

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return Config.model_validate(data)


def parse_legacy_rule(line: str) -> Rule | None:
    """
    Parse a rule from the legacy pipe-delimited format.

    Format: pattern|description|severity|show_source|case_insensitive|logfile|options

    Example:
        Invalid offsets|Invalid offsets error|ERROR|true|false|bot.log
    """
    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    parts = line.split("|")
    if len(parts) < 3:
        return None

    # Parse required fields
    pattern = parts[0].strip()
    description = parts[1].strip()
    severity = parts[2].strip()

    # Parse optional fields with defaults
    show_source = parts[3].strip().lower() == "true" if len(parts) > 3 else False
    case_insensitive = parts[4].strip().lower() == "true" if len(parts) > 4 else False
    source = parts[5].strip() if len(parts) > 5 else "default"

    # Parse extended options (JSON in 7th field)
    options = None
    if len(parts) > 6:
        import json

        try:
            options_json = parts[6].strip()
            if options_json:
                options_data = json.loads(options_json)
                options = RuleOptions.model_validate(options_data)
        except (json.JSONDecodeError, ValueError):
            pass  # Ignore invalid JSON

    return Rule(
        pattern=pattern,
        description=description,
        severity=severity,
        show_source=show_source,
        case_insensitive=case_insensitive,
        source=source,
        options=options,
    )


def load_legacy_config(
    rules_path: Path | str,
    sources: dict[str, Path] | None = None,
) -> Config:
    """
    Load configuration from legacy pipe-delimited format.

    Args:
        rules_path: Path to rules file
        sources: Dict mapping source names to paths

    Returns:
        Config object
    """
    rules_path = Path(rules_path)

    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")

    rules: list[Rule] = []
    with open(rules_path, encoding="utf-8") as f:
        for line in f:
            rule = parse_legacy_rule(line)
            if rule:
                rules.append(rule)

    # Build sources from dict
    log_sources: list[LogSource] = []
    if sources:
        for name, path in sources.items():
            path = Path(path)
            source_type = "directory" if path.is_dir() else "file"
            log_sources.append(
                LogSource(
                    name=name,
                    path=path,
                    type=source_type,
                    pattern="*.log" if source_type == "directory" else None,
                )
            )

    return Config(sources=log_sources, rules=rules)


def convert_legacy_to_yaml(
    rules_path: Path | str,
    sources: dict[str, Path] | None = None,
    output_path: Path | str | None = None,
) -> str:
    """
    Convert legacy config format to YAML.

    Args:
        rules_path: Path to legacy rules file
        sources: Dict mapping source names to paths
        output_path: Optional path to write YAML (if None, returns string)

    Returns:
        YAML string
    """
    config = load_legacy_config(rules_path, sources)

    # Convert to dict for YAML
    data = {
        "sources": [
            {
                "name": s.name,
                "path": str(s.path),
                "type": s.type,
                **({"pattern": s.pattern} if s.pattern else {}),
            }
            for s in config.sources
        ],
        "rules": [],
    }

    for rule in config.rules:
        rule_dict: dict[str, Any] = {
            "pattern": rule.pattern,
            "description": rule.description,
            "severity": rule.severity.value,
        }

        if rule.show_source:
            rule_dict["show_source"] = True
        if rule.case_insensitive:
            rule_dict["case_insensitive"] = True
        if rule.source != "default":
            rule_dict["source"] = rule.source
        if rule.options:
            rule_dict["options"] = rule.options.model_dump(exclude_none=True)

        data["rules"].append(rule_dict)

    yaml_content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if output_path:
        output_path = Path(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(yaml_content)

    return yaml_content

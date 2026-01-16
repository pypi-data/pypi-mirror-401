"""
Core log analysis engine for logowatch.

The LogAnalyzer class provides pattern-based log analysis with:
- Regex pattern matching
- Context extraction (lines before/after)
- Value extraction from matches
- Aggregation by extracted values
- Incremental detection (new errors only)
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from typing import Any, Iterator

from logowatch.config import Config
from logowatch.models import (
    AnalysisCache,
    AnalysisResult,
    JsonParseOptions,
    LogSource,
    Match,
    Rule,
    RuleResult,
    Severity,
    TimestampConfig,
)


class LogAnalyzer:
    """
    Main log analysis engine.

    Analyzes log files based on configured rules and produces structured results.
    Supports incremental analysis to show only new errors since last check.
    """

    def __init__(
        self,
        config: Config,
        cache_path: Path | None = None,
        incremental: bool = True,
    ) -> None:
        """
        Initialize the analyzer.

        Args:
            config: Configuration with sources and rules
            cache_path: Path to store incremental cache (default: .logowatch_cache.json)
            incremental: Enable incremental mode (only show new errors)
        """
        self.config = config
        self.cache_path = cache_path or Path(".logowatch_cache.json")
        self.incremental = incremental
        self._cache: AnalysisCache | None = None
        self._timestamp_patterns: dict[str, re.Pattern] = {}  # Cache for compiled timestamp patterns

    @property
    def cache(self) -> AnalysisCache:
        """Get or load the cache."""
        if self._cache is None:
            self._cache = self._load_cache()
        return self._cache

    def _load_cache(self) -> AnalysisCache:
        """Load cache from file or create new one."""
        if self.cache_path.exists():
            try:
                data = json.loads(self.cache_path.read_text())
                return AnalysisCache.model_validate(data)
            except (json.JSONDecodeError, ValueError):
                pass
        return AnalysisCache()

    def _save_cache(self) -> None:
        """Save cache to file."""
        if self._cache:
            self.cache_path.write_text(
                json.dumps(self._cache.model_dump(mode="json"), indent=2, default=str)
            )

    def _get_timestamp_pattern(self, source: LogSource) -> re.Pattern | None:
        """Get or compile cached timestamp regex pattern for a source."""
        if not source.timestamp or not source.timestamp.pattern:
            return None
        if source.name not in self._timestamp_patterns:
            self._timestamp_patterns[source.name] = re.compile(source.timestamp.pattern)
        return self._timestamp_patterns[source.name]

    def _extract_timestamp_string(
        self,
        line: str,
        source: LogSource,
        json_data: dict | None = None,
    ) -> str | None:
        """Extract timestamp string from line using source config."""
        ts_config = source.timestamp
        if not ts_config:
            return None

        # Option 1: JSON field path
        if ts_config.field and json_data:
            value = self._get_nested_value(json_data, ts_config.field)
            return str(value) if value is not None else None

        # Option 2: Regex extraction
        if ts_config.pattern:
            pattern = self._get_timestamp_pattern(source)
            if pattern:
                match = pattern.search(line)
                if match:
                    # Try named group 'ts' first, then first capture group, then full match
                    if "ts" in match.groupdict():
                        return match.group("ts")
                    if match.groups():
                        return match.group(1)
                    return match.group(0)

        # Option 3: Auto-detect (try common patterns)
        if ts_config.auto:
            return self._auto_detect_timestamp(line, json_data)

        return None

    def _auto_detect_timestamp(self, line: str, json_data: dict | None = None) -> str | None:
        """Try to auto-detect timestamp from common formats."""
        # For JSON, try common timestamp field names
        if json_data:
            for field in ("timestamp", "@timestamp", "time", "ts", "datetime", "date"):
                value = self._get_nested_value(json_data, field)
                if value is not None:
                    return str(value)

        # ISO 8601 (most common for structured logs)
        iso_match = re.search(
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?',
            line
        )
        if iso_match:
            return iso_match.group(0)

        # Common log format (nginx, apache): [14/Jan/2026:09:15:32 +0000]
        clf_match = re.search(r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}[^\]]*)\]', line)
        if clf_match:
            return clf_match.group(1)

        # Syslog format: Jan 14 09:15:32
        syslog_match = re.search(r'\b(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\b', line)
        if syslog_match:
            return syslog_match.group(1)

        return None

    def _parse_timestamp(
        self,
        ts_string: str | None,
        source: LogSource,
    ) -> datetime | None:
        """Parse timestamp string to datetime, normalized to UTC if possible."""
        if not ts_string:
            return None

        ts_config = source.timestamp
        default_tz = "UTC"
        if ts_config and ts_config.timezone:
            default_tz = ts_config.timezone

        try:
            tz = ZoneInfo(default_tz)
        except Exception:
            tz = ZoneInfo("UTC")

        try:
            # Option 1: Explicit strptime format
            if ts_config and ts_config.format:
                dt = datetime.strptime(ts_string, ts_config.format)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=tz)
                return dt

            # Option 2: Try ISO 8601 (fromisoformat)
            try:
                # Handle 'Z' suffix which fromisoformat doesn't handle before 3.11
                ts_normalized = ts_string.replace('Z', '+00:00')
                return datetime.fromisoformat(ts_normalized)
            except ValueError:
                pass

            # Option 3: Try dateutil if available (for complex formats)
            try:
                from dateutil import parser as dateutil_parser
                dt = dateutil_parser.parse(ts_string)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=tz)
                return dt
            except ImportError:
                pass
            except Exception:
                pass

        except (ValueError, OSError):
            pass

        return None

    def _get_file_hash(self, path: Path) -> str:
        """Get file hash for change detection (uses mtime + size)."""
        if not path.exists():
            return "missing"
        stat = path.stat()
        return f"{stat.st_mtime}_{stat.st_size}_{stat.st_ino}"

    def _get_files_for_source(self, source: LogSource) -> Iterator[Path]:
        """Get all files for a log source."""
        path = Path(source.path)

        if source.type == "file":
            if path.exists():
                yield path
        elif source.type == "directory":
            if path.is_dir():
                pattern = source.pattern or "*.log"
                yield from sorted(path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        elif source.type == "glob":
            if source.pattern:
                yield from sorted(Path().glob(source.pattern), key=lambda p: p.stat().st_mtime, reverse=True)

    def _read_file_lines(
        self,
        path: Path,
        start_line: int = 0,
        encoding: str = "utf-8",
    ) -> list[str]:
        """Read file lines, optionally starting from a specific line."""
        try:
            with open(path, encoding=encoding, errors="replace") as f:
                lines = f.readlines()
            if start_line > 0:
                return lines[start_line:]
            return lines
        except OSError:
            return []

    def _match_pattern(
        self,
        pattern: str,
        line: str,
        case_insensitive: bool = False,
    ) -> re.Match[str] | None:
        """Match a pattern against a line."""
        flags = re.IGNORECASE if case_insensitive else 0
        try:
            return re.search(pattern, line, flags)
        except re.error:
            return None

    def _extract_value(self, pattern: str, line: str) -> str | None:
        """Extract value using regex with capture group."""
        try:
            match = re.search(pattern, line)
            if match:
                # Return first capture group if exists, else full match
                groups = match.groups()
                return groups[0] if groups else match.group(0)
        except re.error:
            pass
        return None

    def _parse_json_line(self, line: str) -> dict | None:
        """Parse a JSON/JSONL line, returning None if invalid."""
        line = line.strip()
        if not line:
            return None
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

    def _get_nested_value(self, data: dict, key: str) -> Any:
        """
        Get value from nested dict/list using dot notation and array indexing.

        Examples:
            'user.name' -> data['user']['name']
            'items[0]' -> data['items'][0]
            'content[0].text' -> data['content'][0]['text']
            'messages[-1].role' -> data['messages'][-1]['role']
            'content[?type=text].text' -> first element where type=="text", then .text
            'content[?type=text][0].text' -> same (explicit first)
        """
        import re

        # Handle array filter syntax: field[?filterKey=filterValue]
        # Convert to intermediate form for processing
        filter_pattern = r'\[\?(\w+)=([^\]]+)\]'

        def apply_array_filter(arr: list, filter_key: str, filter_value: str) -> Any:
            """Find first element in array where filter_key == filter_value."""
            for item in arr:
                if isinstance(item, dict) and item.get(filter_key) == filter_value:
                    return item
            return None

        # Process the key, handling filter syntax
        current = data
        remaining_key = key

        while remaining_key:
            # Check for array filter at current position
            filter_match = re.match(r'^([^.\[\]]*)\[\?(\w+)=([^\]]+)\](.*)$', remaining_key)
            if filter_match:
                field_name = filter_match.group(1)
                filter_key = filter_match.group(2)
                filter_value = filter_match.group(3)
                remaining_key = filter_match.group(4).lstrip('.')

                # Access field if specified
                if field_name:
                    if isinstance(current, dict) and field_name in current:
                        current = current[field_name]
                    else:
                        return None

                # Apply filter
                if isinstance(current, list):
                    current = apply_array_filter(current, filter_key, filter_value)
                    if current is None:
                        return None
                else:
                    return None
                continue

            # Check for regular field access with optional index
            regular_match = re.match(r'^([^.\[\]]+)(?:\[(-?\d+)\])?(.*)$', remaining_key)
            if regular_match:
                field_name = regular_match.group(1)
                index = regular_match.group(2)
                remaining_key = regular_match.group(3).lstrip('.')

                # Access dict field
                if isinstance(current, dict) and field_name in current:
                    current = current[field_name]
                elif isinstance(current, dict):
                    return None
                else:
                    return None

                # Access array index if specified
                if index:
                    idx = int(index)
                    if isinstance(current, list):
                        if -len(current) <= idx < len(current):
                            current = current[idx]
                        else:
                            return None
                    else:
                        return None
                continue

            # No pattern matched, break
            break

        return current

    def _evaluate_filter(self, data: dict, filter_expr: str) -> bool:
        """
        Evaluate a filter expression against JSON data.

        Supports:
            .field == "value"
            .field != "value"
            .field in ["a", "b"]
            .field contains "substring"
            .field starts_with "prefix"
            .field not_starts_with "prefix"
            .field exists
            .field > 100 (numeric)
            .field >= 100
            .field < 100
            .field <= 100

        Combining with AND:
            '.type == "user" && .message.content not_starts_with "[{"'
        """
        if not filter_expr:
            return True

        filter_expr = filter_expr.strip()

        # Handle AND (&&) combinations
        if " && " in filter_expr:
            parts = filter_expr.split(" && ")
            return all(self._evaluate_single_filter(data, p.strip()) for p in parts)

        return self._evaluate_single_filter(data, filter_expr)

    def _evaluate_single_filter(self, data: dict, filter_expr: str) -> bool:
        """Evaluate a single filter expression."""
        if not filter_expr:
            return True

        filter_expr = filter_expr.strip()

        # Parse the expression
        # Pattern: .field operator value
        def str_or_empty(val: Any) -> str:
            """Convert value to string, treating None as empty string."""
            return str(val) if val is not None else ""

        patterns = [
            # .field == "value" or .field == 123
            (r'^\.(\S+)\s*==\s*"([^"]*)"$', lambda d, f, v: str_or_empty(self._get_nested_value(d, f)) == v),
            (r'^\.(\S+)\s*==\s*(\d+)$', lambda d, f, v: self._get_nested_value(d, f) == int(v)),
            # .field != "value"
            (r'^\.(\S+)\s*!=\s*"([^"]*)"$', lambda d, f, v: str_or_empty(self._get_nested_value(d, f)) != v),
            # .field in ["a", "b"]
            (r'^\.(\S+)\s+in\s+\[([^\]]+)\]$', lambda d, f, v: str(self._get_nested_value(d, f)) in [x.strip().strip('"\'') for x in v.split(",")]),
            # .field contains "substring"
            (r'^\.(\S+)\s+contains\s+"([^"]*)"$', lambda d, f, v: v in str(self._get_nested_value(d, f) or "")),
            # .field starts_with "prefix"
            (r'^\.(\S+)\s+starts_with\s+"([^"]*)"$', lambda d, f, v: str(self._get_nested_value(d, f) or "").startswith(v)),
            # .field not_starts_with "prefix"
            (r'^\.(\S+)\s+not_starts_with\s+"([^"]*)"$', lambda d, f, v: not str(self._get_nested_value(d, f) or "").startswith(v)),
            # .field exists (not None/empty)
            (r'^\.(\S+)\s+exists$', lambda d, f, v: self._get_nested_value(d, f) is not None and self._get_nested_value(d, f) != ""),
            # Numeric comparisons
            (r'^\.(\S+)\s*>\s*(\d+)$', lambda d, f, v: (self._get_nested_value(d, f) or 0) > int(v)),
            (r'^\.(\S+)\s*>=\s*(\d+)$', lambda d, f, v: (self._get_nested_value(d, f) or 0) >= int(v)),
            (r'^\.(\S+)\s*<\s*(\d+)$', lambda d, f, v: (self._get_nested_value(d, f) or 0) < int(v)),
            (r'^\.(\S+)\s*<=\s*(\d+)$', lambda d, f, v: (self._get_nested_value(d, f) or 0) <= int(v)),
        ]

        for pattern, evaluator in patterns:
            match = re.match(pattern, filter_expr)
            if match:
                field = match.group(1)
                # Some patterns (like 'exists') don't have a value group
                value = match.group(2) if match.lastindex >= 2 else None
                try:
                    return evaluator(data, field, value)
                except (TypeError, ValueError):
                    return False

        # If no pattern matched, return True (pass through)
        return True

    def _format_json_display(
        self,
        data: dict,
        json_opts: JsonParseOptions,
    ) -> str:
        """Format JSON data for display using template or field list."""
        if json_opts.display:
            # Use format template: "{timestamp} [{level}] {msg}"
            result = json_opts.display
            for key in json_opts.fields or data.keys():
                value = self._get_nested_value(data, key)
                result = result.replace(f"{{{key}}}", str(value) if value is not None else "")
            return result
        elif json_opts.fields:
            # Just show extracted fields
            parts = []
            for key in json_opts.fields:
                value = self._get_nested_value(data, key)
                if value is not None:
                    parts.append(f"{key}={value}")
            return " | ".join(parts)
        else:
            # Compact JSON representation
            return json.dumps(data, ensure_ascii=False)

    def _match_json_line(
        self,
        line: str,
        rule: Rule,
    ) -> tuple[bool, dict | None, str | None]:
        """
        Match a JSON line against a rule.

        Returns:
            (matched, json_data, formatted_content)
        """
        data = self._parse_json_line(line)
        if data is None:
            return False, None, None

        json_opts = rule.options.json_parse if rule.options else None

        # Apply filter if specified
        if json_opts and json_opts.filter:
            if not self._evaluate_filter(data, json_opts.filter):
                return False, None, None

        # Apply pattern matching (can match on any field value)
        if rule.pattern != ".":
            # Convert JSON to string for pattern matching
            json_str = json.dumps(data, ensure_ascii=False)
            if not self._match_pattern(rule.pattern, json_str, rule.case_insensitive):
                return False, None, None

        # Format for display
        formatted = None
        if json_opts:
            formatted = self._format_json_display(data, json_opts)

        return True, data, formatted

    def _get_context(
        self,
        all_lines: list[str],
        line_idx: int,
        before: int = 0,
        after: int = 0,
    ) -> tuple[list[str], list[str]]:
        """Get context lines before and after a match."""
        start = max(0, line_idx - before)
        end = min(len(all_lines), line_idx + after + 1)

        context_before = [l.rstrip() for l in all_lines[start:line_idx]]
        context_after = [l.rstrip() for l in all_lines[line_idx + 1:end]]

        return context_before, context_after

    def _find_related(
        self,
        all_lines: list[str],
        line_idx: int,
        pattern: str,
        lines: int = 3,
        direction: str = "after",
    ) -> list[str]:
        """Find related patterns near a match."""
        related: list[str] = []

        if direction in ("before", "both"):
            start = max(0, line_idx - lines)
            for i in range(start, line_idx):
                if re.search(pattern, all_lines[i]):
                    related.append(all_lines[i].rstrip())

        if direction in ("after", "both"):
            end = min(len(all_lines), line_idx + lines + 1)
            for i in range(line_idx + 1, end):
                if re.search(pattern, all_lines[i]):
                    related.append(all_lines[i].rstrip())

        return related

    def _analyze_rule(
        self,
        rule: Rule,
        source: LogSource,
        all_lines: list[str],
        file_path: Path,
        start_line: int = 0,
    ) -> RuleResult:
        """Analyze a single rule against file lines."""
        matches: list[Match] = []
        aggregations: Counter[str] = Counter()
        related_patterns: list[str] = []
        total_count = 0

        # Options
        options = rule.options
        context_before = options.context.before if options and options.context else 0
        context_after = options.context.after if options and options.context else 0

        # Check if JSON format
        is_json_format = rule.format in ("json", "jsonl")

        for idx, line in enumerate(all_lines):
            # Match based on format
            json_data: dict | None = None
            formatted_content: str | None = None

            if is_json_format:
                matched, json_data, formatted_content = self._match_json_line(line, rule)
                if not matched:
                    continue
            else:
                if not self._match_pattern(rule.pattern, line, rule.case_insensitive):
                    continue

            total_count += 1
            actual_line_num = start_line + idx + 1

            # Limit matches stored in memory
            if len(matches) < 100:
                ctx_before, ctx_after = self._get_context(
                    all_lines, idx, context_before, context_after
                )

                # Extract values if configured
                extracted: dict[str, str] = {}
                if options and options.extract:
                    value = self._extract_value(options.extract.pattern, line)
                    if value:
                        extracted[options.extract.name] = value

                # For JSON, also extract from json_opts.fields
                if json_data and options and options.json_parse and options.json_parse.fields:
                    for field in options.json_parse.fields:
                        value = self._get_nested_value(json_data, field)
                        if value is not None:
                            extracted[field] = str(value)

                # Find related patterns
                if options and options.find_related:
                    related = self._find_related(
                        all_lines,
                        idx,
                        options.find_related.pattern,
                        options.find_related.lines,
                        options.find_related.direction,
                    )
                    related_patterns.extend(related)

                # Extract and parse timestamp for sorting
                ts_string = self._extract_timestamp_string(line, source, json_data)
                parsed_ts = self._parse_timestamp(ts_string, source)

                matches.append(
                    Match(
                        rule_id=rule.id,
                        line_number=actual_line_num,
                        content=line.rstrip(),
                        formatted_content=formatted_content,
                        source_file=file_path,
                        context_before=ctx_before,
                        context_after=ctx_after,
                        extracted_values=extracted,
                        json_data=json_data,
                        parsed_timestamp=parsed_ts,
                        source_name=source.name,
                    )
                )

            # Aggregate if configured
            if options and options.aggregate:
                if json_data:
                    # For JSON, can aggregate by field value
                    agg_value = self._get_nested_value(json_data, options.aggregate.by.lstrip("."))
                    if agg_value is not None:
                        aggregations[str(agg_value)] += 1
                else:
                    agg_value = self._extract_value(options.aggregate.by, line)
                    if agg_value:
                        aggregations[agg_value] += 1

        return RuleResult(
            rule=rule,
            total_count=total_count,
            new_count=total_count,  # All are "new" relative to start_line
            matches=matches,
            aggregations=dict(aggregations.most_common(50)),
            related_patterns=list(set(related_patterns))[:20],
        )

    def analyze(
        self,
        source_names: list[str] | None = None,
        max_examples: int = 20,
    ) -> AnalysisResult:
        """
        Run the analysis.

        Args:
            source_names: Specific sources to analyze (None = all)
            max_examples: Maximum examples to include per rule

        Returns:
            AnalysisResult with all findings
        """
        result = AnalysisResult(
            timestamp=datetime.now(),
            incremental=self.incremental,
            last_check=self.cache.last_check,
        )

        # Determine which sources to analyze
        sources = self.config.sources
        if source_names:
            sources = [s for s in sources if s.name in source_names]

        for source in sources:
            result.sources_analyzed.append(source.name)
            rules = self.config.get_rules_for_source(source.name)

            for file_path in self._get_files_for_source(source):
                file_hash = self._get_file_hash(file_path)
                cached_lines = 0

                if self.incremental:
                    cached_lines = self.cache.get_cached_line_count(str(file_path), file_hash)

                # Read all lines for context
                all_lines = self._read_file_lines(file_path, encoding=source.encoding)
                result.total_lines += len(all_lines)

                # For incremental, only analyze new lines
                lines_to_analyze = all_lines[cached_lines:] if cached_lines > 0 else all_lines
                start_line = cached_lines

                for rule in rules:
                    rule_result = self._analyze_rule(
                        rule, source, lines_to_analyze, file_path, start_line
                    )

                    if rule_result.total_count > 0:
                        # Limit examples (0 = unlimited)
                        if max_examples > 0:
                            rule_result.matches = rule_result.matches[:max_examples]

                        # Update severity counts
                        if rule.severity == Severity.ERROR:
                            result.total_errors += rule_result.total_count
                        elif rule.severity == Severity.WARNING:
                            result.total_warnings += rule_result.total_count
                        else:
                            result.total_info += rule_result.total_count

                        result.rule_results.append(rule_result)

                # Update cache
                if self.incremental:
                    self.cache.update_entry(str(file_path), len(all_lines), file_hash)

        # Save cache
        if self.incremental:
            self._save_cache()

        return result

    def analyze_file(
        self,
        file_path: Path | str,
        rules: list[Rule] | None = None,
    ) -> AnalysisResult:
        """
        Analyze a single file with specified rules.

        Args:
            file_path: Path to the log file
            rules: Rules to apply (default: all rules)

        Returns:
            AnalysisResult with findings
        """
        file_path = Path(file_path)
        rules = rules or self.config.rules

        result = AnalysisResult(
            timestamp=datetime.now(),
            sources_analyzed=[str(file_path)],
        )

        all_lines = self._read_file_lines(file_path)
        result.total_lines = len(all_lines)

        dummy_source = LogSource(name="direct", path=file_path, type="file")

        for rule in rules:
            rule_result = self._analyze_rule(rule, dummy_source, all_lines, file_path)

            if rule_result.total_count > 0:
                if rule.severity == Severity.ERROR:
                    result.total_errors += rule_result.total_count
                elif rule.severity == Severity.WARNING:
                    result.total_warnings += rule_result.total_count
                else:
                    result.total_info += rule_result.total_count

                result.rule_results.append(rule_result)

        return result

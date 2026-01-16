"""
Data models for logowatch.

Uses Pydantic for validation and serialization of configuration and results.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Severity(str, Enum):
    """Log severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    @classmethod
    def from_string(cls, value: str) -> "Severity":
        """Parse severity from string (case-insensitive)."""
        return cls(value.lower())


class RuleContext(BaseModel):
    """Context lines configuration for a rule."""

    before: int = Field(default=0, ge=0, description="Lines to show before match")
    after: int = Field(default=0, ge=0, description="Lines to show after match")


class RuleExtract(BaseModel):
    """Value extraction configuration."""

    pattern: str = Field(description="Regex pattern with capture group")
    name: str = Field(default="value", description="Name for the extracted value")


class RuleFindRelated(BaseModel):
    """Find related pattern configuration."""

    pattern: str = Field(description="Pattern to find nearby")
    lines: int = Field(default=3, ge=1, description="Lines to search within")
    direction: str = Field(
        default="after", pattern="^(before|after|both)$", description="Search direction"
    )


class RuleAggregate(BaseModel):
    """Aggregation configuration."""

    by: str = Field(description="Regex pattern for grouping (with capture group)")
    format: str = Field(default="count", description="Output format")


class JsonParseOptions(BaseModel):
    """JSON/JSONL parsing configuration for structured log lines."""

    fields: list[str] = Field(
        default_factory=list,
        description="JSON keys to extract (e.g., ['level', 'msg', 'timestamp'])",
    )
    filter: str | None = Field(
        default=None,
        description="Simple filter expression (e.g., '.level == \"ERROR\"')",
    )
    display: str | None = Field(
        default=None,
        description="Display format template (e.g., '{timestamp} [{level}] {msg}')",
    )


class TimestampConfig(BaseModel):
    """Timestamp extraction configuration for a log source."""

    pattern: str | None = Field(default=None, description="Regex pattern with named group 'ts' for timestamp")
    format: str | None = Field(default=None, description="strptime format string (e.g., '%Y-%m-%dT%H:%M:%S')")
    field: str | None = Field(default=None, description="JSON field path for timestamp (e.g., 'timestamp', '@timestamp')")
    timezone: str = Field(default="UTC", description="Default timezone if not in log")
    auto: bool = Field(default=False, description="Auto-detect common timestamp formats")


class RuleOptions(BaseModel):
    """Extended options for a rule."""

    context: RuleContext | None = None
    extract: RuleExtract | None = None
    find_related: RuleFindRelated | None = None
    aggregate: RuleAggregate | None = None
    json_parse: JsonParseOptions | None = Field(
        default=None,
        alias="json",
        description="JSON/JSONL parsing options for structured logs",
    )


class Rule(BaseModel):
    """A single log analysis rule."""

    id: str | None = Field(default=None, description="Unique rule identifier")
    pattern: str = Field(description="Regex pattern to match")
    description: str = Field(description="Human-readable description")
    format: str = Field(
        default="text",
        pattern="^(text|json|jsonl)$",
        description="Log format: 'text' (default), 'json', or 'jsonl'",
    )
    severity: Severity = Field(default=Severity.INFO, description="Severity level")
    section: str | None = Field(
        default=None,
        description="Custom section heading (e.g., 'Performance', 'Security'). If not set, groups by severity.",
    )
    show_source: bool = Field(
        default=False, description="Show source file:line if detectable"
    )
    case_insensitive: bool = Field(default=False, description="Case-insensitive matching")
    source: str = Field(default="default", description="Log source name")
    options: RuleOptions | None = Field(default=None, description="Extended options")
    enabled: bool = Field(default=True, description="Whether rule is active")
    tags: list[str] = Field(default_factory=list, description="Tags for filtering")

    @field_validator("severity", mode="before")
    @classmethod
    def parse_severity(cls, v: Any) -> Severity:
        if isinstance(v, str):
            return Severity.from_string(v)
        return v


class LogSource(BaseModel):
    """Configuration for a log source."""

    name: str = Field(description="Unique name for the source")
    path: Path = Field(description="Path to log file or directory")
    type: str = Field(
        default="file", pattern="^(file|directory|glob)$", description="Source type"
    )
    pattern: str | None = Field(
        default=None, description="Glob pattern for directory/glob types"
    )
    encoding: str = Field(default="utf-8", description="File encoding")
    timestamp: TimestampConfig | None = Field(default=None, description="Timestamp extraction config")


class Match(BaseModel):
    """A single match result."""

    rule_id: str | None = Field(default=None, description="Rule that matched")
    line_number: int = Field(description="Line number in log file")
    content: str = Field(description="Matched line content (raw)")
    formatted_content: str | None = Field(
        default=None,
        description="Formatted content for display (used with JSON format)",
    )
    source_file: Path = Field(description="Source log file")
    context_before: list[str] = Field(default_factory=list)
    context_after: list[str] = Field(default_factory=list)
    extracted_values: dict[str, str] = Field(default_factory=dict)
    json_data: dict[str, Any] | None = Field(
        default=None,
        description="Parsed JSON data from the log line",
    )
    source_location: str | None = Field(
        default=None, description="Source code location (file:line)"
    )
    parsed_timestamp: datetime | None = Field(
        default=None,
        description="Parsed and normalized timestamp for chronological sorting",
    )
    source_name: str = Field(
        default="default",
        description="Source name for multi-source display",
    )


class RuleResult(BaseModel):
    """Results for a single rule."""

    rule: Rule
    total_count: int = Field(default=0, description="Total matches")
    new_count: int = Field(default=0, description="New matches since last check")
    matches: list[Match] = Field(default_factory=list, description="Sample matches")
    aggregations: dict[str, int] = Field(
        default_factory=dict, description="Aggregated counts"
    )
    related_patterns: list[str] = Field(
        default_factory=list, description="Related patterns found"
    )


class AnalysisResult(BaseModel):
    """Complete analysis result."""

    timestamp: datetime = Field(default_factory=datetime.now)
    sources_analyzed: list[str] = Field(default_factory=list)
    total_lines: int = Field(default=0)
    total_errors: int = Field(default=0)
    total_warnings: int = Field(default=0)
    total_info: int = Field(default=0)
    rule_results: list[RuleResult] = Field(default_factory=list)
    incremental: bool = Field(default=False, description="Whether incremental mode was used")
    last_check: datetime | None = Field(default=None)

    @property
    def has_critical_issues(self) -> bool:
        """Check if there are any ERROR level matches."""
        return self.total_errors > 0

    def get_results_by_severity(self, severity: Severity) -> list[RuleResult]:
        """Get rule results filtered by severity."""
        return [r for r in self.rule_results if r.rule.severity == severity]


class CacheEntry(BaseModel):
    """Cache entry for incremental detection."""

    source_path: str
    line_count: int
    file_hash: str
    last_check: datetime


class AnalysisCache(BaseModel):
    """Cache for incremental analysis."""

    version: int = Field(default=2)
    last_check: datetime | None = None
    entries: dict[str, CacheEntry] = Field(default_factory=dict)

    def get_cached_line_count(self, source_path: str, current_hash: str) -> int:
        """Get cached line count if hash matches, else 0."""
        entry = self.entries.get(source_path)
        if entry and entry.file_hash == current_hash:
            return entry.line_count
        return 0

    def update_entry(self, source_path: str, line_count: int, file_hash: str) -> None:
        """Update or create cache entry."""
        self.entries[source_path] = CacheEntry(
            source_path=source_path,
            line_count=line_count,
            file_hash=file_hash,
            last_check=datetime.now(),
        )
        self.last_check = datetime.now()

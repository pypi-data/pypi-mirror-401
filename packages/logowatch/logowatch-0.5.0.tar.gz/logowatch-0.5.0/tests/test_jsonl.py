"""Tests for JSON/JSONL log parsing."""

import tempfile
from pathlib import Path

import pytest

from logowatch import LogAnalyzer, Rule, LogSource, Config, Severity
from logowatch.models import RuleOptions, JsonParseOptions


@pytest.fixture
def jsonl_log_file():
    """Create a temporary JSONL log file."""
    content = """{"timestamp": "2024-01-01T10:00:00", "level": "INFO", "message": "Application started", "user_id": 100}
{"timestamp": "2024-01-01T10:00:01", "level": "DEBUG", "message": "Processing request", "user_id": 123}
{"timestamp": "2024-01-01T10:00:02", "level": "ERROR", "message": "Failed to process: timeout", "user_id": 123, "error_code": 504}
{"timestamp": "2024-01-01T10:00:03", "level": "WARNING", "message": "Connection retry attempt", "user_id": 456}
{"timestamp": "2024-01-01T10:00:04", "level": "ERROR", "message": "Database connection failed", "user_id": 456, "error_code": 500}
{"timestamp": "2024-01-01T10:00:05", "level": "INFO", "message": "Retrying...", "user_id": 456}
{"timestamp": "2024-01-01T10:00:06", "level": "ERROR", "message": "Database connection failed again", "user_id": 789, "error_code": 500}
{"timestamp": "2024-01-01T10:00:07", "level": "INFO", "message": "Cleanup complete", "user_id": 100}
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(content)
        return Path(f.name)


def test_jsonl_basic_filter(jsonl_log_file):
    """Test basic JSONL filtering by field value."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="JSON Errors",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["timestamp", "level", "message"],
                        filter='.level == "ERROR"',
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    # Should find 3 ERROR lines
    assert result.total_errors == 3
    assert len(result.rule_results) == 1
    rule_result = result.rule_results[0]
    assert rule_result.total_count == 3


def test_jsonl_display_format(jsonl_log_file):
    """Test formatted display output."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="Formatted Errors",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["timestamp", "level", "message"],
                        filter='.level == "ERROR"',
                        display="{timestamp} [{level}] {message}",
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    assert len(result.rule_results) == 1
    rule_result = result.rule_results[0]

    # Check formatted content
    assert rule_result.matches[0].formatted_content is not None
    assert "[ERROR]" in rule_result.matches[0].formatted_content
    assert "Failed to process" in rule_result.matches[0].formatted_content


def test_jsonl_field_extraction(jsonl_log_file):
    """Test extracting fields from JSON."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="Extract user_id",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["user_id", "error_code"],
                        filter='.level == "ERROR"',
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    rule_result = result.rule_results[0]

    # Check extracted values include user_id
    first_match = rule_result.matches[0]
    assert "user_id" in first_match.extracted_values
    assert first_match.extracted_values["user_id"] == "123"


def test_jsonl_aggregation(jsonl_log_file):
    """Test aggregation by JSON field."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="Aggregate by error_code",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["error_code"],
                        filter='.level == "ERROR"',
                    ),
                    aggregate={"by": ".error_code"},
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    rule_result = result.rule_results[0]

    # Should have aggregations by error_code
    assert len(rule_result.aggregations) > 0
    # Two errors have 500, one has 504
    assert "500" in rule_result.aggregations
    assert rule_result.aggregations["500"] == 2


def test_jsonl_numeric_filter(jsonl_log_file):
    """Test numeric comparison in filter."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="User ID > 200",
                severity=Severity.INFO,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["user_id", "message"],
                        filter=".user_id > 200",
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    # Users 456 and 789 are > 200
    assert result.total_info > 0
    for match in result.rule_results[0].matches:
        user_id = int(match.extracted_values.get("user_id", 0))
        assert user_id > 200


def test_jsonl_contains_filter(jsonl_log_file):
    """Test contains filter for substring matching."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="Messages containing 'Database'",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["message"],
                        filter='.message contains "Database"',
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    # Two messages contain "Database"
    assert result.total_errors == 2


def test_jsonl_in_filter(jsonl_log_file):
    """Test 'in' filter for multiple values."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="ERROR or WARNING",
                severity=Severity.WARNING,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["level", "message"],
                        filter='.level in ["ERROR", "WARNING"]',
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    # 3 ERROR + 1 WARNING = 4
    assert result.total_warnings == 4


def test_jsonl_with_regex_pattern(jsonl_log_file):
    """Test combining JSON format with regex pattern."""
    config = Config(
        sources=[LogSource(name="test", path=jsonl_log_file, type="file")],
        rules=[
            Rule(
                pattern="Database",  # Regex on JSON content
                format="jsonl",
                description="Database-related JSON entries",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["message", "error_code"],
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    # Two entries mention "Database"
    assert result.total_errors == 2


def test_jsonl_nested_field():
    """Test nested field extraction (dot notation)."""
    content = """{"timestamp": "2024-01-01", "user": {"id": 123, "name": "Alice"}, "action": "login"}
{"timestamp": "2024-01-02", "user": {"id": 456, "name": "Bob"}, "action": "logout"}
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(content)
        path = Path(f.name)

    config = Config(
        sources=[LogSource(name="test", path=path, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="Nested field test",
                severity=Severity.INFO,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(
                        fields=["user.id", "user.name", "action"],
                        display="{user.name} ({user.id}): {action}",
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    assert result.total_info == 2
    # Check formatted content has nested values
    first_match = result.rule_results[0].matches[0]
    assert "Alice" in first_match.formatted_content
    assert "123" in first_match.formatted_content


def test_invalid_json_lines_skipped(jsonl_log_file, tmp_path):
    """Test that invalid JSON lines are gracefully skipped."""
    # Create file with mix of valid and invalid JSON
    content = """{"level": "ERROR", "message": "Valid error"}
not valid json at all
{"level": "INFO", "message": "Valid info"}
{ broken json {
{"level": "ERROR", "message": "Another valid error"}
"""
    log_file = tmp_path / "mixed.log"
    log_file.write_text(content)

    config = Config(
        sources=[LogSource(name="test", path=log_file, type="file")],
        rules=[
            Rule(
                pattern=".",
                format="jsonl",
                description="All JSON entries",
                severity=Severity.INFO,
                source="test",
                options=RuleOptions(
                    json=JsonParseOptions(fields=["level", "message"])
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    # Should only match the 3 valid JSON lines
    assert result.total_info == 3

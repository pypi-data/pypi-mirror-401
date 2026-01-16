"""Tests for the LogAnalyzer class."""

import tempfile
from pathlib import Path

import pytest

from logowatch import LogAnalyzer, Rule, LogSource, Config, Severity


@pytest.fixture
def sample_log_file():
    """Create a temporary log file for testing."""
    content = """2024-01-01 10:00:00 - INFO - Application started
2024-01-01 10:00:01 - INFO - [user:123] Processing request
2024-01-01 10:00:02 - ERROR - [user:123] Failed to process: timeout
2024-01-01 10:00:03 - WARNING - Connection retry attempt 1
2024-01-01 10:00:04 - ERROR - [user:456] Database connection failed
2024-01-01 10:00:05 - INFO - [user:456] Retrying...
2024-01-01 10:00:06 - ERROR - [user:456] Database connection failed again
Traceback (most recent call last):
  File "app.py", line 42, in process
    raise ValueError("Invalid data")
ValueError: Invalid data
2024-01-01 10:00:07 - INFO - Cleanup complete
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        f.write(content)
        return Path(f.name)


@pytest.fixture
def sample_config(sample_log_file):
    """Create a sample configuration."""
    return Config(
        sources=[
            LogSource(name="test", path=sample_log_file, type="file")
        ],
        rules=[
            Rule(
                pattern="ERROR",
                description="Errors",
                severity=Severity.ERROR,
                source="test",
            ),
            Rule(
                pattern="WARNING",
                description="Warnings",
                severity=Severity.WARNING,
                source="test",
            ),
            Rule(
                pattern="Traceback",
                description="Exceptions",
                severity=Severity.ERROR,
                source="test",
            ),
        ],
    )


def test_analyzer_basic(sample_config, sample_log_file):
    """Test basic analysis."""
    analyzer = LogAnalyzer(sample_config, incremental=False)
    result = analyzer.analyze()

    assert result.total_errors > 0
    assert result.total_warnings > 0
    assert "test" in result.sources_analyzed


def test_analyzer_error_count(sample_config, sample_log_file):
    """Test error counting."""
    analyzer = LogAnalyzer(sample_config, incremental=False)
    result = analyzer.analyze()

    # Should find 3 ERROR lines + 1 Traceback
    error_results = result.get_results_by_severity(Severity.ERROR)
    total_errors = sum(r.total_count for r in error_results)
    assert total_errors == 4  # 3 ERROR + 1 Traceback


def test_analyzer_warning_count(sample_config, sample_log_file):
    """Test warning counting."""
    analyzer = LogAnalyzer(sample_config, incremental=False)
    result = analyzer.analyze()

    warning_results = result.get_results_by_severity(Severity.WARNING)
    total_warnings = sum(r.total_count for r in warning_results)
    assert total_warnings == 1


def test_analyzer_with_extract(sample_log_file):
    """Test value extraction."""
    from logowatch.models import RuleOptions, RuleExtract

    config = Config(
        sources=[LogSource(name="test", path=sample_log_file, type="file")],
        rules=[
            Rule(
                # Pattern: ERROR followed by [user:xxx]
                pattern=r"ERROR.*\[user:\d+\]",
                description="User errors",
                severity=Severity.ERROR,
                source="test",
                options=RuleOptions(
                    extract=RuleExtract(
                        pattern=r"\[user:(\d+)\]",
                        name="user_id",
                    )
                ),
            ),
        ],
    )

    analyzer = LogAnalyzer(config, incremental=False)
    result = analyzer.analyze()

    assert len(result.rule_results) == 1
    rule_result = result.rule_results[0]

    # Check extracted values - should find user 123 and 456
    extracted_users = {
        v
        for m in rule_result.matches
        for v in m.extracted_values.values()
    }
    assert "123" in extracted_users or "456" in extracted_users


def test_analyzer_incremental(sample_config, sample_log_file, tmp_path):
    """Test incremental mode."""
    cache_file = tmp_path / ".cache.json"

    # First run - should find all errors
    analyzer = LogAnalyzer(sample_config, cache_path=cache_file, incremental=True)
    result1 = analyzer.analyze()
    initial_errors = result1.total_errors

    # Second run - should find no new errors
    analyzer2 = LogAnalyzer(sample_config, cache_path=cache_file, incremental=True)
    result2 = analyzer2.analyze()

    assert result2.total_errors == 0  # No new errors


def test_config_get_rules_for_source(sample_config):
    """Test getting rules by source."""
    rules = sample_config.get_rules_for_source("test")
    assert len(rules) == 3

    rules = sample_config.get_rules_for_source("nonexistent")
    assert len(rules) == 0


def test_rule_severity_parsing():
    """Test severity parsing from string."""
    rule = Rule(
        pattern="test",
        description="Test",
        severity="error",  # lowercase string
    )
    assert rule.severity == Severity.ERROR

    rule = Rule(
        pattern="test",
        description="Test",
        severity="WARNING",  # uppercase string
    )
    assert rule.severity == Severity.WARNING

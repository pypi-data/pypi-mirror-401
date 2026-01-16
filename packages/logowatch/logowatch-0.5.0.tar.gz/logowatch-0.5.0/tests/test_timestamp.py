"""
Tests for timestamp extraction and parsing features.

Tests cover:
- TimestampConfig model validation
- JSON field extraction
- Regex timestamp extraction
- Auto-detect mode
- strptime format parsing
- Multi-source merge sort
- Missing timestamp handling
- Backwards compatibility
"""

import pytest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from logowatch.models import TimestampConfig, LogSource, Match
from logowatch.config import OutputConfig, Config
from logowatch.analyzer import LogAnalyzer


class TestTimestampConfigModel:
    """Test TimestampConfig Pydantic model."""

    def test_default_values(self):
        """Test default values are correct."""
        ts_config = TimestampConfig()
        assert ts_config.pattern is None
        assert ts_config.format is None
        assert ts_config.field is None
        assert ts_config.timezone == "UTC"
        assert ts_config.auto is False

    def test_json_field_config(self):
        """Test JSON field configuration."""
        ts_config = TimestampConfig(field="timestamp")
        assert ts_config.field == "timestamp"

    def test_regex_config(self):
        """Test regex pattern configuration."""
        ts_config = TimestampConfig(
            pattern=r'^(?P<ts>\d{4}-\d{2}-\d{2})',
            format="%Y-%m-%d",
        )
        assert ts_config.pattern is not None
        assert ts_config.format == "%Y-%m-%d"

    def test_auto_detect_config(self):
        """Test auto-detect configuration."""
        ts_config = TimestampConfig(auto=True)
        assert ts_config.auto is True


class TestLogSourceWithTimestamp:
    """Test LogSource with timestamp config."""

    def test_source_without_timestamp(self):
        """Test source without timestamp config (backwards compatible)."""
        source = LogSource(name="test", path=Path("/tmp/test.log"))
        assert source.timestamp is None

    def test_source_with_timestamp_field(self):
        """Test source with JSON timestamp field."""
        source = LogSource(
            name="test",
            path=Path("/tmp/test.log"),
            timestamp=TimestampConfig(field="timestamp"),
        )
        assert source.timestamp is not None
        assert source.timestamp.field == "timestamp"


class TestMatchWithTimestamp:
    """Test Match model with timestamp fields."""

    def test_match_default_values(self):
        """Test Match has default timestamp fields."""
        match = Match(
            line_number=1,
            content="test line",
            source_file=Path("/tmp/test.log"),
        )
        assert match.parsed_timestamp is None
        assert match.source_name == "default"

    def test_match_with_timestamp(self):
        """Test Match with parsed timestamp."""
        ts = datetime(2026, 1, 14, 9, 15, 32, tzinfo=ZoneInfo("UTC"))
        match = Match(
            line_number=1,
            content="test line",
            source_file=Path("/tmp/test.log"),
            parsed_timestamp=ts,
            source_name="api",
        )
        assert match.parsed_timestamp == ts
        assert match.source_name == "api"


class TestOutputConfigSortBy:
    """Test OutputConfig sort_by field."""

    def test_default_sort_by(self):
        """Test default sort_by is line_number."""
        output = OutputConfig()
        assert output.sort_by == "line_number"

    def test_timestamp_sort_by(self):
        """Test timestamp sort_by."""
        output = OutputConfig(sort_by="timestamp")
        assert output.sort_by == "timestamp"

    def test_invalid_sort_by(self):
        """Test invalid sort_by raises validation error."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            OutputConfig(sort_by="invalid")


class TestTimestampExtraction:
    """Test timestamp extraction in analyzer."""

    @pytest.fixture
    def analyzer(self, tmp_path):
        """Create analyzer with minimal config."""
        config = Config(
            sources=[
                LogSource(
                    name="test",
                    path=tmp_path / "test.log",
                    timestamp=TimestampConfig(field="timestamp"),
                )
            ],
            rules=[],
        )
        return LogAnalyzer(config, incremental=False)

    def test_extract_json_timestamp(self, analyzer):
        """Test extracting timestamp from JSON field."""
        source = analyzer.config.sources[0]
        json_data = {"timestamp": "2026-01-14T09:15:32Z"}

        ts_string = analyzer._extract_timestamp_string("", source, json_data)
        assert ts_string == "2026-01-14T09:15:32Z"

    def test_auto_detect_iso8601(self, analyzer):
        """Test auto-detect of ISO 8601 timestamp."""
        source = LogSource(
            name="auto",
            path=Path("/tmp/test.log"),
            timestamp=TimestampConfig(auto=True),
        )

        ts_string = analyzer._auto_detect_timestamp(
            "2026-01-14T09:15:32.123Z INFO message",
            None
        )
        assert ts_string == "2026-01-14T09:15:32.123Z"

    def test_auto_detect_common_log_format(self, analyzer):
        """Test auto-detect of common log format."""
        ts_string = analyzer._auto_detect_timestamp(
            '[14/Jan/2026:09:15:32 +0000] "GET /api" 200',
            None
        )
        assert ts_string == "14/Jan/2026:09:15:32 +0000"


class TestTimestampParsing:
    """Test timestamp parsing."""

    @pytest.fixture
    def analyzer(self, tmp_path):
        """Create analyzer with minimal config."""
        config = Config(sources=[], rules=[])
        return LogAnalyzer(config, incremental=False)

    def test_parse_iso8601(self, analyzer):
        """Test parsing ISO 8601 timestamp."""
        source = LogSource(
            name="test",
            path=Path("/tmp/test.log"),
            timestamp=TimestampConfig(),
        )

        dt = analyzer._parse_timestamp("2026-01-14T09:15:32+00:00", source)
        assert dt is not None
        assert dt.year == 2026
        assert dt.month == 1
        assert dt.day == 14

    def test_parse_iso8601_with_z(self, analyzer):
        """Test parsing ISO 8601 with Z suffix."""
        source = LogSource(
            name="test",
            path=Path("/tmp/test.log"),
            timestamp=TimestampConfig(),
        )

        dt = analyzer._parse_timestamp("2026-01-14T09:15:32Z", source)
        assert dt is not None

    def test_parse_with_explicit_format(self, analyzer):
        """Test parsing with explicit strptime format."""
        source = LogSource(
            name="test",
            path=Path("/tmp/test.log"),
            timestamp=TimestampConfig(format="%Y-%m-%d %H:%M:%S"),
        )

        dt = analyzer._parse_timestamp("2026-01-14 09:15:32", source)
        assert dt is not None
        assert dt.hour == 9
        assert dt.minute == 15

    def test_parse_none_returns_none(self, analyzer):
        """Test parsing None returns None."""
        source = LogSource(name="test", path=Path("/tmp/test.log"))

        dt = analyzer._parse_timestamp(None, source)
        assert dt is None

    def test_parse_invalid_returns_none(self, analyzer):
        """Test parsing invalid string returns None."""
        source = LogSource(
            name="test",
            path=Path("/tmp/test.log"),
            timestamp=TimestampConfig(format="%Y-%m-%d"),
        )

        dt = analyzer._parse_timestamp("not-a-date", source)
        assert dt is None


class TestBackwardsCompatibility:
    """Test backwards compatibility with existing configs."""

    def test_config_without_timestamp(self):
        """Test config without any timestamp settings still works."""
        config = Config(
            sources=[
                LogSource(name="test", path=Path("/tmp/test.log"))
            ],
            rules=[],
        )

        # Should not raise
        assert config.sources[0].timestamp is None
        assert config.output.sort_by == "line_number"

    def test_output_without_sort_by(self):
        """Test output config without sort_by uses default."""
        output = OutputConfig()
        assert output.sort_by == "line_number"

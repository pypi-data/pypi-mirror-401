"""
Logowatch - Autonomous log analysis with configurable pattern rules.

A powerful log analysis tool that scans log files for patterns defined in
configuration files and provides rich, colored output with context,
aggregations, and incremental detection.

Usage:
    from logowatch import LogAnalyzer, load_config

    config = load_config("logowatch.yaml")
    analyzer = LogAnalyzer(config)
    result = analyzer.analyze()
"""

from logowatch.analyzer import LogAnalyzer
from logowatch.models import (
    Rule,
    RuleContext,
    RuleExtract,
    RuleFindRelated,
    RuleAggregate,
    RuleOptions,
    JsonParseOptions,
    LogSource,
    AnalysisResult,
    RuleResult,
    Match,
    Severity,
    AnalysisCache,
)
from logowatch.config import (
    Config,
    OutputConfig,
    load_config,
    load_legacy_config,
    discover_config,
    CONFIG_FILE_NAMES,
)

__version__ = "0.4.3"
__all__ = [
    "LogAnalyzer",
    "Rule",
    "RuleContext",
    "RuleExtract",
    "RuleFindRelated",
    "RuleAggregate",
    "RuleOptions",
    "JsonParseOptions",
    "LogSource",
    "AnalysisResult",
    "RuleResult",
    "Match",
    "Severity",
    "AnalysisCache",
    "Config",
    "OutputConfig",
    "load_config",
    "load_legacy_config",
    "discover_config",
    "CONFIG_FILE_NAMES",
]

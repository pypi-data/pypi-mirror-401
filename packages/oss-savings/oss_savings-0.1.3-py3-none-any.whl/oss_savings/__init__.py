"""OSS Savings Calculator - Estimate development cost savings from open source."""

__version__ = "0.1.0"

from oss_savings.calculator import (
    analyze_repo,
    RepoStats,
    RiskAssessment,
    DEFAULT_HOURLY_RATE,
)

__all__ = [
    "analyze_repo",
    "RepoStats",
    "RiskAssessment",
    "DEFAULT_HOURLY_RATE",
]

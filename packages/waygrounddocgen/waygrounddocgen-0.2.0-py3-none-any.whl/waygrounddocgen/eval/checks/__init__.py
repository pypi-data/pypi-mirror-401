"""
Automated documentation checks.

These checks run fast, deterministic validations against documentation.
"""

from .coverage import CoverageChecker
from .structure import StructureChecker
from .freshness import FreshnessChecker

__all__ = ["CoverageChecker", "StructureChecker", "FreshnessChecker"]

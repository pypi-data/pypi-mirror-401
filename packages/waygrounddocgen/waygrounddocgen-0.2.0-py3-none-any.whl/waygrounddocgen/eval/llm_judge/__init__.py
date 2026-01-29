"""
LLM-as-Judge evaluation components.

Uses Claude to evaluate documentation quality against source code.
"""

from .judge import LLMJudge

__all__ = ["LLMJudge"]

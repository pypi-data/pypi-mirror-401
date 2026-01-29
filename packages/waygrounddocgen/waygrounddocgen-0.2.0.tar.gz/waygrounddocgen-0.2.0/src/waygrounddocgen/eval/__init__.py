"""
waygrounddocgen.eval - Documentation evaluation module

Evaluates generated documentation against modules.json source of truth.

Flow:
1. Load modules.json (logical groupings)
2. For each module, run:
   - Phase 1: Automated checks (coverage, structure, freshness)
   - Phase 2: LLM-as-judge (if Phase 1 passes)
3. If evaluation fails and auto-retry is enabled:
   - Regenerate with feedback (max 2 attempts)
   - Re-evaluate
4. Generate report
"""

from .evaluator import DocumentationEvaluator

__all__ = ["DocumentationEvaluator"]


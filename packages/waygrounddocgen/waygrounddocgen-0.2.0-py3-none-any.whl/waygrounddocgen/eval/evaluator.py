#!/usr/bin/env python3
"""
evaluator.py - Documentation Evaluation Orchestrator

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

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import evaluation components
from .checks.coverage import CoverageChecker
from .checks.structure import StructureChecker
from .checks.freshness import FreshnessChecker
from .llm_judge.judge import LLMJudge
from .retry.feedback_loop import FeedbackLoop


def get_default_config_path() -> Path:
    """Get the path to the default config.yaml within the package."""
    return Path(__file__).parent / "config.yaml"


class DocumentationEvaluator:
    """
    Main orchestrator for documentation evaluation.

    Combines automated checks and LLM-as-judge evaluation
    with optional auto-retry functionality.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        repo_path: Optional[str] = None,
    ):
        """
        Initialize the evaluator.

        Args:
            config_path: Path to config.yaml
            repo_path: Path to repository root
        """
        self.repo_path = repo_path or os.getcwd()
        self.config = self._load_config(config_path)

        # Initialize checkers
        self.coverage_checker = CoverageChecker(self.config.get("coverage", {}))
        self.structure_checker = StructureChecker(self.config.get("structure", {}))
        self.freshness_checker = FreshnessChecker(
            self.config.get("freshness", {}),
            self.repo_path
        )
        self.llm_judge = LLMJudge(self.config.get("llm_judge", {}))
        self.feedback_loop = FeedbackLoop(self.config.get("retry", {}))

        # Thresholds
        self.require_llm_pass = self.config.get("require_llm_pass", True)
        self.skip_freshness = self.config.get("skip_freshness", False)

    def _load_config(self, config_path: Optional[str]) -> dict:
        """Load configuration from file or use defaults."""
        # Try provided path first
        if config_path and os.path.exists(config_path):
            try:
                import yaml
                with open(config_path) as f:
                    return yaml.safe_load(f) or {}
            except ImportError:
                # Fall back to JSON if yaml not available
                if config_path.endswith('.json'):
                    with open(config_path) as f:
                        return json.load(f)
        
        # Try default config in package
        default_config = get_default_config_path()
        if default_config.exists():
            try:
                import yaml
                with open(default_config) as f:
                    return yaml.safe_load(f) or {}
            except ImportError:
                pass
        
        return {}

    def load_modules(self, modules_path: str) -> list:
        """Load modules from modules.json file."""
        with open(modules_path) as f:
            data = json.load(f)

        # Support both "logical_modules" and "modules" keys
        return data.get("logical_modules", data.get("modules", data.get("components", [])))

    def evaluate_module(
        self,
        module: dict,
        doc_content: str,
        run_llm: bool = True,
        source_code: Optional[str] = None,
    ) -> dict:
        """
        Evaluate documentation for a single module.

        Args:
            module: Module definition from modules.json
            doc_content: Content of the generated documentation
            run_llm: Whether to run LLM evaluation
            source_code: Optional source code for accuracy checking

        Returns:
            dict with evaluation results
        """
        module_name = module.get("name", "Unknown")
        results = {
            "module": module_name,
            "timestamp": datetime.now().isoformat(),
            "passed": False,
            "phase1_passed": False,
            "phase2_passed": None,  # None if not run
            "scores": {},
            "issues": [],
        }

        print(f"\n{'='*50}")
        print(f"Evaluating: {module_name}")
        print(f"{'='*50}")

        # ============================================
        # PHASE 1: Automated Checks
        # ============================================
        print("\n[Phase 1] Running automated checks...")

        # Coverage check
        print("  - Coverage check...", end=" ")
        coverage_result = self.coverage_checker.evaluate(module, doc_content)
        results["coverage"] = coverage_result.to_dict()
        results["scores"]["coverage"] = coverage_result.score
        print(f"{'PASS' if coverage_result.passed else 'FAIL'} ({coverage_result.score:.2f})")

        if not coverage_result.passed:
            results["issues"].append({
                "type": "coverage",
                "message": f"Coverage score {coverage_result.score:.2f} below threshold",
                "details": coverage_result.to_dict().get("missing", {}),
            })

        # Structure check
        print("  - Structure check...", end=" ")
        structure_result = self.structure_checker.evaluate(module, doc_content)
        results["structure"] = structure_result.to_dict()
        results["scores"]["structure"] = structure_result.score
        print(f"{'PASS' if structure_result.passed else 'FAIL'} ({structure_result.score:.2f})")

        if not structure_result.passed:
            results["issues"].append({
                "type": "structure",
                "message": f"Structure score {structure_result.score:.2f} below threshold",
                "details": structure_result.issues,
            })

        # Freshness check (optional)
        if not self.skip_freshness:
            doc_path = module.get("expected_doc_path", "")
            if doc_path and os.path.exists(os.path.join(self.repo_path, doc_path)):
                print("  - Freshness check...", end=" ")
                freshness_result = self.freshness_checker.evaluate(
                    module,
                    os.path.join(self.repo_path, doc_path)
                )
                results["freshness"] = freshness_result.to_dict()
                results["scores"]["freshness"] = freshness_result.score
                print(f"{'PASS' if freshness_result.passed else 'WARN'} ({freshness_result.score:.2f})")
            else:
                print("  - Freshness check... SKIP (no doc file)")

        # Phase 1 result
        phase1_passed = coverage_result.passed and structure_result.passed
        results["phase1_passed"] = phase1_passed

        if not phase1_passed:
            print(f"\n[Phase 1] FAILED - Skipping Phase 2")
            results["passed"] = False
            return results

        print(f"\n[Phase 1] PASSED")

        # ============================================
        # PHASE 2: LLM-as-Judge
        # ============================================
        if not run_llm:
            print("\n[Phase 2] Skipped (--no-llm flag)")
            results["phase2_passed"] = None
            results["passed"] = phase1_passed
            return results

        if not self.llm_judge.client:
            print("\n[Phase 2] Skipped (no API key)")
            results["phase2_passed"] = None
            results["passed"] = phase1_passed
            return results

        print("\n[Phase 2] Running LLM evaluation...")
        llm_result = self.llm_judge.evaluate(module, doc_content, source_code)
        results["llm_judge"] = llm_result.to_dict()
        results["scores"]["accuracy"] = llm_result.accuracy_score
        results["scores"]["completeness"] = llm_result.completeness_score
        results["scores"]["clarity"] = llm_result.clarity_score
        results["scores"]["llm_overall"] = llm_result.overall_score

        print(f"  - Accuracy:     {llm_result.accuracy_score}/5")
        print(f"  - Completeness: {llm_result.completeness_score}/5")
        print(f"  - Clarity:      {llm_result.clarity_score}/5")
        print(f"  - Overall:      {llm_result.overall_score:.2f}")

        results["phase2_passed"] = llm_result.passed

        if not llm_result.passed:
            results["issues"].append({
                "type": "llm_judge",
                "message": "LLM evaluation below threshold",
                "details": {
                    "accuracy_issues": llm_result.accuracy_issues,
                    "completeness_issues": llm_result.completeness_issues,
                    "clarity_issues": llm_result.clarity_issues,
                    "suggestions": llm_result.suggestions,
                },
            })

        print(f"\n[Phase 2] {'PASSED' if llm_result.passed else 'FAILED'}")

        # Final result
        if self.require_llm_pass:
            results["passed"] = phase1_passed and llm_result.passed
        else:
            results["passed"] = phase1_passed

        return results

    def evaluate_with_retry(
        self,
        module: dict,
        doc_content: str,
        max_retries: int = 2,
        source_code: Optional[str] = None,
    ) -> dict:
        """
        Evaluate with automatic retry on failure.

        Args:
            module: Module definition
            doc_content: Documentation content
            max_retries: Maximum retry attempts (default: 2)
            source_code: Optional source code

        Returns:
            dict with evaluation results and retry info
        """
        # Initial evaluation
        results = self.evaluate_module(module, doc_content, source_code=source_code)

        if results["passed"]:
            results["retry_attempted"] = False
            return results

        # Retry if failed
        print(f"\n{'='*50}")
        print("STARTING RETRY LOOP")
        print(f"{'='*50}")

        def evaluate_fn(mod, doc):
            return self.evaluate_module(mod, doc, source_code=source_code)

        retry_result = self.feedback_loop.retry_with_feedback(
            module=module,
            current_doc=doc_content,
            eval_results=results,
            evaluate_fn=evaluate_fn,
            source_code=source_code,
        )

        results["retry_attempted"] = True
        results["retry_result"] = retry_result.to_dict()

        if retry_result.success:
            # Re-run final evaluation to get complete results
            final_results = self.evaluate_module(
                module,
                retry_result.new_content,
                source_code=source_code,
            )
            final_results["retry_attempted"] = True
            final_results["retry_result"] = retry_result.to_dict()
            final_results["regenerated_content"] = retry_result.new_content
            return final_results

        return results

    def evaluate_all(
        self,
        modules_path: str,
        docs_dir: str,
        auto_retry: bool = False,
        max_retries: int = 2,
        run_llm: bool = True,
        save_fixes: bool = False,
    ) -> dict:
        """
        Evaluate all modules.

        Args:
            modules_path: Path to modules.json
            docs_dir: Directory containing generated docs
            auto_retry: Enable automatic retry on failure
            max_retries: Maximum retry attempts
            run_llm: Whether to run LLM evaluation
            save_fixes: Save regenerated docs to disk when auto-retry succeeds

        Returns:
            dict with all evaluation results
        """
        modules = self.load_modules(modules_path)

        print(f"\nLoaded {len(modules)} modules from {modules_path}")
        print(f"Docs directory: {docs_dir}")
        print(f"Auto-retry: {auto_retry} (max: {max_retries})")
        print(f"LLM evaluation: {run_llm}")

        results = {
            "timestamp": datetime.now().isoformat(),
            "modules_file": modules_path,
            "docs_dir": docs_dir,
            "config": {
                "auto_retry": auto_retry,
                "max_retries": max_retries,
                "run_llm": run_llm,
            },
            "modules": [],
            "summary": {
                "total": len(modules),
                "passed": 0,
                "failed": 0,
                "skipped": 0,
            },
        }

        for module in modules:
            module_name = module.get("name", "Unknown")
            slug = module.get("slug", module_name.lower().replace(" ", "-"))
            doc_path = module.get("expected_doc_path", f"{docs_dir}/{slug}.md")

            # Check if doc exists
            full_doc_path = os.path.join(self.repo_path, doc_path)
            if not os.path.exists(full_doc_path):
                print(f"\n[SKIP] {module_name} - Doc not found: {doc_path}")
                results["modules"].append({
                    "module": module_name,
                    "status": "skipped",
                    "reason": f"Doc not found: {doc_path}",
                })
                results["summary"]["skipped"] += 1
                continue

            # Read documentation
            with open(full_doc_path, encoding="utf-8") as f:
                doc_content = f.read()

            # Evaluate
            if auto_retry:
                module_result = self.evaluate_with_retry(
                    module, doc_content, max_retries
                )
                # Save fixed doc if requested and retry succeeded
                if save_fixes and module_result.get("regenerated_content"):
                    fixed_doc_path = os.path.join(self.repo_path, doc_path)
                    with open(fixed_doc_path, "w", encoding="utf-8") as f:
                        f.write(module_result["regenerated_content"])
                    print(f"  [SAVED] Fixed documentation written to: {doc_path}")
            else:
                module_result = self.evaluate_module(
                    module, doc_content, run_llm=run_llm
                )

            results["modules"].append(module_result)

            if module_result.get("passed"):
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1

        # Overall pass/fail
        results["overall_pass"] = results["summary"]["failed"] == 0

        return results


def print_summary(results: dict):
    """Print a summary of evaluation results."""
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    summary = results.get("summary", {})
    print(f"\nTotal modules: {summary.get('total', 0)}")
    print(f"  Passed:  {summary.get('passed', 0)}")
    print(f"  Failed:  {summary.get('failed', 0)}")
    print(f"  Skipped: {summary.get('skipped', 0)}")

    print(f"\nOverall: {'PASS' if results.get('overall_pass') else 'FAIL'}")

    # Show failed modules
    failed = [m for m in results.get("modules", []) if not m.get("passed") and m.get("status") != "skipped"]
    if failed:
        print("\nFailed modules:")
        for m in failed:
            print(f"  - {m.get('module')}")
            for issue in m.get("issues", [])[:3]:
                print(f"    * {issue.get('type')}: {issue.get('message')}")


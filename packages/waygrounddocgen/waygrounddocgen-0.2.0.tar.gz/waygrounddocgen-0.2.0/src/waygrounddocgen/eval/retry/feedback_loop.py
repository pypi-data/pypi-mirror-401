"""
Feedback Loop - Automatic documentation regeneration with evaluation feedback.

When documentation fails evaluation, this module:
1. Collects all issues from evaluation results
2. Builds a feedback prompt with specific issues
3. Triggers regeneration with the feedback context
4. Re-evaluates the new documentation
5. Repeats up to MAX_RETRIES times
"""

import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

try:
    import anthropic
except ImportError:
    anthropic = None


@dataclass
class RegenerationResult:
    """Result of a regeneration attempt."""
    success: bool
    attempt: int
    max_attempts: int

    # New documentation (if successful)
    new_content: Optional[str] = None

    # Evaluation results per attempt
    attempts: list = field(default_factory=list)

    # Final status
    final_scores: dict = field(default_factory=dict)
    remaining_issues: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "attempt": self.attempt,
            "max_attempts": self.max_attempts,
            "attempts": self.attempts,
            "final_scores": self.final_scores,
            "remaining_issues": self.remaining_issues,
        }


class FeedbackLoop:
    """
    Manages the feedback loop for documentation regeneration.

    Flow:
    1. Receive failing evaluation results
    2. Build feedback prompt with issues
    3. Call regeneration function (provided by user)
    4. Re-evaluate
    5. Repeat if still failing (up to max_retries)
    """

    # Maximum retry attempts (user specified: 2)
    MAX_RETRIES = 2

    def __init__(
        self,
        config: Optional[dict] = None,
        regenerate_fn: Optional[Callable] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize the feedback loop.

        Args:
            config: Optional config dict
            regenerate_fn: Function to call for regeneration
                           Signature: (module, feedback_prompt) -> new_doc_content
            api_key: Anthropic API key for built-in regeneration
        """
        self.config = config or {}
        self.regenerate_fn = regenerate_fn

        # API setup for built-in regeneration
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = None
        if anthropic and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        # Config
        self.max_retries = self.config.get("max_retries", self.MAX_RETRIES)
        self.model = self.config.get("model", "claude-sonnet-4-20250514")

    def retry_with_feedback(
        self,
        module: dict,
        current_doc: str,
        eval_results: dict,
        evaluate_fn: Callable,
        source_code: Optional[str] = None,
    ) -> RegenerationResult:
        """
        Attempt to regenerate documentation with feedback.

        Args:
            module: Module definition from modules.json
            current_doc: Current failing documentation
            eval_results: Evaluation results with issues
            evaluate_fn: Function to evaluate documentation
                         Signature: (module, doc_content) -> eval_results
            source_code: Optional source code for context

        Returns:
            RegenerationResult with success status and attempts
        """
        attempts = []
        doc_content = current_doc

        for attempt in range(1, self.max_retries + 1):
            # Build feedback prompt from issues
            feedback = self._build_feedback_prompt(module, doc_content, eval_results)

            # Log attempt
            attempt_record = {
                "attempt": attempt,
                "timestamp": datetime.now().isoformat(),
                "issues_addressed": self._extract_issues(eval_results),
            }

            # Regenerate documentation
            try:
                if self.regenerate_fn:
                    # Use provided regeneration function
                    new_doc = self.regenerate_fn(module, feedback)
                else:
                    # Use built-in regeneration
                    new_doc = self._regenerate_with_claude(
                        module, doc_content, feedback, source_code
                    )

                if not new_doc:
                    attempt_record["status"] = "regeneration_failed"
                    attempt_record["error"] = "Empty response from regeneration"
                    attempts.append(attempt_record)
                    continue

                doc_content = new_doc
                attempt_record["regenerated"] = True

            except Exception as e:
                attempt_record["status"] = "regeneration_error"
                attempt_record["error"] = str(e)
                attempts.append(attempt_record)
                continue

            # Re-evaluate
            try:
                eval_results = evaluate_fn(module, doc_content)
                attempt_record["eval_results"] = {
                    "passed": eval_results.get("passed", False),
                    "scores": eval_results.get("scores", {}),
                }

                if eval_results.get("passed", False):
                    attempt_record["status"] = "success"
                    attempts.append(attempt_record)

                    return RegenerationResult(
                        success=True,
                        attempt=attempt,
                        max_attempts=self.max_retries,
                        new_content=doc_content,
                        attempts=attempts,
                        final_scores=eval_results.get("scores", {}),
                        remaining_issues=[],
                    )
                else:
                    attempt_record["status"] = "still_failing"
                    attempts.append(attempt_record)

            except Exception as e:
                attempt_record["status"] = "eval_error"
                attempt_record["error"] = str(e)
                attempts.append(attempt_record)

        # All retries exhausted
        return RegenerationResult(
            success=False,
            attempt=self.max_retries,
            max_attempts=self.max_retries,
            new_content=doc_content,
            attempts=attempts,
            final_scores=eval_results.get("scores", {}),
            remaining_issues=self._extract_issues(eval_results),
        )

    def _build_feedback_prompt(
        self,
        module: dict,
        current_doc: str,
        eval_results: dict,
    ) -> str:
        """Build a feedback prompt from evaluation results."""
        module_name = module.get("name", "Unknown")
        issues = self._extract_issues(eval_results)

        feedback = f"""# Documentation Regeneration Request

## Module: {module_name}

The previous documentation generation had the following issues that need to be addressed:

## Issues to Fix

"""
        # Group issues by type
        coverage_issues = eval_results.get("coverage", {}).get("missing", {})
        structure_issues = eval_results.get("structure", {}).get("issues", [])
        llm_issues = eval_results.get("llm_judge", {}).get("issues", {})

        # Coverage issues
        if coverage_issues:
            feedback += "### Coverage Gaps\n\n"

            if coverage_issues.get("entry_points"):
                feedback += "**Missing Entry Points:**\n"
                for ep in coverage_issues["entry_points"][:5]:
                    feedback += f"- {ep}\n"
                feedback += "\n"

            if coverage_issues.get("endpoints"):
                feedback += "**Missing API Endpoints:**\n"
                for ep in coverage_issues["endpoints"][:5]:
                    feedback += f"- {ep}\n"
                feedback += "\n"

            if coverage_issues.get("structs"):
                feedback += "**Missing Data Structures:**\n"
                for s in coverage_issues["structs"][:5]:
                    feedback += f"- {s}\n"
                feedback += "\n"

        # Structure issues
        if structure_issues:
            feedback += "### Structure Issues\n\n"
            for issue in structure_issues[:5]:
                feedback += f"- {issue}\n"
            feedback += "\n"

        # LLM judge issues
        if llm_issues:
            if llm_issues.get("accuracy"):
                feedback += "### Accuracy Issues\n\n"
                for issue in llm_issues["accuracy"][:3]:
                    feedback += f"- {issue}\n"
                feedback += "\n"

            if llm_issues.get("completeness"):
                feedback += "### Completeness Issues\n\n"
                for issue in llm_issues["completeness"][:3]:
                    feedback += f"- {issue}\n"
                feedback += "\n"

            if llm_issues.get("clarity"):
                feedback += "### Clarity Issues\n\n"
                for issue in llm_issues["clarity"][:3]:
                    feedback += f"- {issue}\n"
                feedback += "\n"

        # Suggestions
        suggestions = eval_results.get("llm_judge", {}).get("suggestions", [])
        if suggestions:
            feedback += "### Suggestions for Improvement\n\n"
            for suggestion in suggestions[:5]:
                feedback += f"- {suggestion}\n"
            feedback += "\n"

        feedback += """
## Instructions

Please regenerate the documentation addressing ALL the issues above. Ensure:
1. All missing entry points and endpoints are documented
2. All structural issues are fixed
3. Accuracy issues are corrected
4. The documentation is clear and complete

Focus specifically on the issues mentioned - do not remove content that was already correct.
"""

        return feedback

    def _extract_issues(self, eval_results: dict) -> list:
        """Extract all issues from evaluation results into a flat list."""
        issues = []

        # Coverage issues
        coverage = eval_results.get("coverage", {}).get("missing", {})
        for key, items in coverage.items():
            for item in items:
                issues.append(f"Missing {key}: {item}")

        # Structure issues
        for issue in eval_results.get("structure", {}).get("issues", []):
            issues.append(f"Structure: {issue}")

        # LLM judge issues
        llm = eval_results.get("llm_judge", {}).get("issues", {})
        for category, items in llm.items():
            for item in items:
                issues.append(f"{category.title()}: {item}")

        return issues

    def _regenerate_with_claude(
        self,
        module: dict,
        current_doc: str,
        feedback: str,
        source_code: Optional[str] = None,
    ) -> Optional[str]:
        """
        Regenerate documentation using Claude API.

        This is the built-in regeneration when no custom function is provided.
        """
        if not self.client:
            return None

        module_name = module.get("name", "Unknown")
        module_desc = module.get("description", "")

        # Build prompt
        prompt = f"""You are regenerating documentation for a software module based on feedback.

## Module: {module_name}
{module_desc}

## Current Documentation (with issues)

{current_doc}

{feedback}

## Expected Elements

**Entry Points:** {', '.join(module.get('entry_points', [])[:10])}
**API Endpoints:** {self._format_endpoints(module.get('api_endpoints', []))}
**Data Structures:** {', '.join(module.get('structs', [])[:10])}

"""

        if source_code:
            prompt += f"""
## Source Code Reference

```
{source_code[:20000]}
```
"""

        prompt += """
## Output

Generate improved documentation in Markdown format. Address all the issues mentioned above.
Start directly with the module title (# ModuleName) - no preamble.
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text if response.content else None

        except Exception as e:
            print(f"Regeneration error: {e}")
            return None

    def _format_endpoints(self, endpoints: list) -> str:
        """Format endpoints for display."""
        if not endpoints:
            return "None specified"

        lines = []
        for ep in endpoints[:10]:
            method = ep.get("method", "?")
            path = ep.get("path", "?")
            lines.append(f"{method} {path}")

        return ", ".join(lines)


def main():
    """Test the feedback loop."""
    print("Feedback Loop Module")
    print(f"Max retries: {FeedbackLoop.MAX_RETRIES}")

    # Example eval results with issues
    eval_results = {
        "passed": False,
        "coverage": {
            "missing": {
                "entry_points": ["AuthService.Logout"],
                "endpoints": ["POST /auth/refresh"],
            }
        },
        "structure": {
            "issues": ["Missing Data Models section"]
        },
        "llm_judge": {
            "issues": {
                "accuracy": ["Wrong HTTP method for login endpoint"],
                "completeness": ["Token refresh flow not documented"],
            },
            "suggestions": [
                "Add sequence diagram for auth flow",
                "Document error responses",
            ]
        }
    }

    loop = FeedbackLoop()
    feedback = loop._build_feedback_prompt(
        {"name": "Authentication"},
        "# Auth\n\nSome content...",
        eval_results,
    )

    print("\nGenerated Feedback Prompt:")
    print("-" * 40)
    print(feedback)


if __name__ == "__main__":
    main()

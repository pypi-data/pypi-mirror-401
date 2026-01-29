"""
LLM-as-Judge - Uses Claude to evaluate documentation quality.

Evaluates:
- Accuracy: Are facts correct? No hallucinations?
- Completeness: Is everything important documented?
- Clarity: Is it understandable?
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import anthropic
except ImportError:
    anthropic = None


@dataclass
class JudgeResult:
    """Result of LLM judge evaluation."""
    passed: bool

    # Scores (1-5 scale)
    accuracy_score: int = 0
    completeness_score: int = 0
    clarity_score: int = 0
    overall_score: float = 0.0

    # Detailed feedback
    accuracy_issues: list = field(default_factory=list)
    completeness_issues: list = field(default_factory=list)
    clarity_issues: list = field(default_factory=list)

    # Suggestions for improvement
    suggestions: list = field(default_factory=list)

    # Raw response (for debugging)
    raw_response: str = ""

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "scores": {
                "accuracy": self.accuracy_score,
                "completeness": self.completeness_score,
                "clarity": self.clarity_score,
                "overall": round(self.overall_score, 2),
            },
            "issues": {
                "accuracy": self.accuracy_issues,
                "completeness": self.completeness_issues,
                "clarity": self.clarity_issues,
            },
            "suggestions": self.suggestions,
        }


class LLMJudge:
    """
    Uses Claude to evaluate documentation quality.

    Performs three types of evaluation:
    1. Accuracy - Compares doc against source code for factual errors
    2. Completeness - Checks if all important aspects are covered
    3. Clarity - Evaluates readability and understandability
    """

    def __init__(self, config: Optional[dict] = None, api_key: Optional[str] = None):
        """
        Initialize the LLM judge.

        Args:
            config: Optional config dict with threshold overrides
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
        """
        self.config = config or {}

        # API setup
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.client = None

        if anthropic and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

        # Model config
        self.model = self.config.get("model", "claude-sonnet-4-20250514")
        self.max_tokens = self.config.get("max_tokens", 2048)

        # Thresholds
        self.min_accuracy = self.config.get("min_accuracy_score", 4)
        self.min_completeness = self.config.get("min_completeness_score", 3)
        self.min_clarity = self.config.get("min_clarity_score", 3)

        # Load prompts
        self.prompts_dir = Path(__file__).parent / "prompts"

    def evaluate(
        self,
        module: dict,
        doc_content: str,
        source_code: Optional[str] = None,
    ) -> JudgeResult:
        """
        Evaluate documentation using LLM judge.

        Args:
            module: Module definition from modules.json
            doc_content: Content of the generated documentation
            source_code: Optional source code for accuracy checking

        Returns:
            JudgeResult with scores and issues
        """
        if not self.client:
            return JudgeResult(
                passed=False,
                accuracy_issues=["LLM judge unavailable: No API key or anthropic not installed"],
            )

        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(module, doc_content, source_code)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            raw_response = response.content[0].text if response.content else ""

            # Parse the response
            result = self._parse_response(raw_response)
            result.raw_response = raw_response

            return result

        except Exception as e:
            return JudgeResult(
                passed=False,
                accuracy_issues=[f"LLM evaluation failed: {str(e)}"],
            )

    def _build_evaluation_prompt(
        self,
        module: dict,
        doc_content: str,
        source_code: Optional[str],
    ) -> str:
        """Build the evaluation prompt."""
        module_name = module.get("name", "Unknown")
        module_desc = module.get("description", "")
        entry_points = module.get("entry_points", [])
        endpoints = module.get("api_endpoints", [])
        structs = module.get("structs", [])

        # Build expected elements section
        expected_elements = f"""
## Expected Elements (from modules.json)

**Entry Points:** {', '.join(entry_points[:10])}
**API Endpoints:**
{self._format_endpoints(endpoints)}
**Data Structures:** {', '.join(structs[:10])}
"""

        # Build source code section if available
        source_section = ""
        if source_code:
            # Truncate if too long
            if len(source_code) > 30000:
                source_code = source_code[:30000] + "\n\n... (truncated)"
            source_section = f"""
## Source Code Reference

```
{source_code}
```
"""

        prompt = f"""You are a documentation quality evaluator. Evaluate the following documentation for a software module.

## Module Information

**Name:** {module_name}
**Description:** {module_desc}

{expected_elements}

## Generated Documentation

{doc_content}

{source_section}

## Evaluation Task

Evaluate the documentation on three dimensions. For each, provide a score (1-5) and specific issues.

### 1. Accuracy (1-5)
- Are the facts correct?
- Do function signatures, API paths, and descriptions match the expected elements?
- Are there any hallucinations or made-up features?

### 2. Completeness (1-5)
- Are all entry points documented?
- Are all API endpoints covered?
- Are data models explained?
- Is the architecture clear?

### 3. Clarity (1-5)
- Is the documentation easy to understand?
- Is it well-organized?
- Are examples helpful?
- Could a new developer understand the module from this doc?

## Output Format

Respond with a JSON object ONLY (no other text):

```json
{{
    "accuracy": {{
        "score": <1-5>,
        "issues": ["list of specific accuracy issues found, or empty if none"]
    }},
    "completeness": {{
        "score": <1-5>,
        "issues": ["list of missing items or gaps"]
    }},
    "clarity": {{
        "score": <1-5>,
        "issues": ["list of clarity problems"]
    }},
    "suggestions": ["list of specific improvements to make the documentation better"]
}}
```

Score meanings:
- 5: Excellent, no issues
- 4: Good, minor issues
- 3: Acceptable, some issues
- 2: Below standard, significant issues
- 1: Poor, major problems

Be specific and actionable in your feedback."""

        return prompt

    def _format_endpoints(self, endpoints: list) -> str:
        """Format endpoints for display."""
        if not endpoints:
            return "None specified"

        lines = []
        for ep in endpoints[:10]:
            method = ep.get("method", "?")
            path = ep.get("path", "?")
            desc = ep.get("description", "")
            lines.append(f"- {method} {path}: {desc}")

        return "\n".join(lines)

    def _parse_response(self, response: str) -> JudgeResult:
        """Parse the LLM response into a JudgeResult."""
        # Try to extract JSON from response
        try:
            # Look for JSON block
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                data = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")

            # Extract scores
            accuracy = data.get("accuracy", {})
            completeness = data.get("completeness", {})
            clarity = data.get("clarity", {})

            accuracy_score = accuracy.get("score", 0)
            completeness_score = completeness.get("score", 0)
            clarity_score = clarity.get("score", 0)

            # Calculate overall (weighted average)
            overall_score = (
                accuracy_score * 0.4 +
                completeness_score * 0.35 +
                clarity_score * 0.25
            )

            # Determine if passed
            passed = (
                accuracy_score >= self.min_accuracy and
                completeness_score >= self.min_completeness and
                clarity_score >= self.min_clarity
            )

            return JudgeResult(
                passed=passed,
                accuracy_score=accuracy_score,
                completeness_score=completeness_score,
                clarity_score=clarity_score,
                overall_score=overall_score,
                accuracy_issues=accuracy.get("issues", []),
                completeness_issues=completeness.get("issues", []),
                clarity_issues=clarity.get("issues", []),
                suggestions=data.get("suggestions", []),
            )

        except (json.JSONDecodeError, ValueError) as e:
            # Return a failed result with parsing error
            return JudgeResult(
                passed=False,
                accuracy_issues=[f"Failed to parse LLM response: {str(e)}"],
            )

    def evaluate_accuracy_only(
        self,
        module: dict,
        doc_content: str,
        source_code: str,
    ) -> dict:
        """
        Quick accuracy-only evaluation.

        Useful for fast checking without full evaluation.
        """
        if not self.client:
            return {"passed": False, "error": "LLM unavailable"}

        prompt = f"""Compare this documentation against the source code. Are there any factual errors?

## Module: {module.get('name', 'Unknown')}

## Documentation:
{doc_content[:10000]}

## Source Code:
{source_code[:20000]}

List any inaccuracies found. If accurate, respond with "ACCURATE".
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            text = response.content[0].text if response.content else ""

            if "ACCURATE" in text.upper() and len(text) < 100:
                return {"passed": True, "issues": []}
            else:
                return {"passed": False, "issues": [text]}

        except Exception as e:
            return {"passed": False, "error": str(e)}


def main():
    """Test the LLM judge."""
    import os

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to test LLM judge")
        return

    # Sample module
    module = {
        "name": "Authentication",
        "description": "User authentication and session management",
        "entry_points": ["NewLoginController", "AuthService.Login"],
        "api_endpoints": [
            {"method": "POST", "path": "/auth/login", "description": "User login"},
        ],
        "structs": ["LoginRequest", "LoginResponse"],
    }

    # Sample doc
    doc_content = """
# Authentication

## Overview
Handles user authentication.

## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/login | User login |

## Data Models
- LoginRequest
- LoginResponse
"""

    judge = LLMJudge()
    result = judge.evaluate(module, doc_content)

    print("LLM Judge Result:")
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()

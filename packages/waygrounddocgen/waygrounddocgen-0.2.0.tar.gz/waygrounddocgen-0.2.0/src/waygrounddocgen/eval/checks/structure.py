"""
Structure checker - validates documentation structure and format.

Checks:
- Required sections are present
- Mermaid diagrams exist
- Tables are properly formatted
- Code blocks are present
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StructureResult:
    """Result of structure evaluation."""
    score: float  # 0.0 to 1.0
    passed: bool

    # Section analysis
    sections_found: list = field(default_factory=list)
    sections_missing: list = field(default_factory=list)
    section_coverage: float = 0.0

    # Format checks
    has_mermaid_diagram: bool = False
    has_tables: bool = False
    has_code_blocks: bool = False
    has_overview: bool = False

    # Quality indicators
    word_count: int = 0
    heading_count: int = 0

    # Issues
    issues: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 3),
            "passed": self.passed,
            "sections": {
                "found": self.sections_found,
                "missing": self.sections_missing,
                "coverage": round(self.section_coverage, 3),
            },
            "format": {
                "has_mermaid_diagram": self.has_mermaid_diagram,
                "has_tables": self.has_tables,
                "has_code_blocks": self.has_code_blocks,
                "has_overview": self.has_overview,
            },
            "quality": {
                "word_count": self.word_count,
                "heading_count": self.heading_count,
            },
            "issues": self.issues,
        }


class StructureChecker:
    """
    Checks documentation structure and format.

    Validates that documentation follows expected structure
    with required sections and proper formatting.
    """

    # Default required sections
    DEFAULT_REQUIRED_SECTIONS = [
        "Overview",
        "Architecture",
        "API Endpoints",
        "Data Models",
        "Dependencies",
    ]

    # Section aliases (alternative names that are acceptable)
    SECTION_ALIASES = {
        "overview": ["overview", "introduction", "summary", "about"],
        "architecture": ["architecture", "design", "structure", "system design"],
        "api endpoints": ["api endpoints", "apis", "endpoints", "http endpoints", "rest api", "api reference"],
        "data models": ["data models", "models", "schemas", "data structures", "entities", "types"],
        "dependencies": ["dependencies", "external dependencies", "integrations", "related services"],
        "error handling": ["error handling", "errors", "error codes", "exceptions"],
        "usage examples": ["usage examples", "examples", "usage", "code examples"],
        "configuration": ["configuration", "config", "environment variables", "settings"],
    }

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize with optional config overrides.

        Args:
            config: Optional config dict with threshold overrides
        """
        self.config = config or {}

        # Thresholds
        self.min_section_coverage = self.config.get("min_section_coverage", 0.8)
        self.require_mermaid = self.config.get("require_mermaid", False)
        self.require_tables = self.config.get("require_tables", False)
        self.require_code_blocks = self.config.get("require_code_blocks", True)
        self.min_word_count = self.config.get("min_word_count", 200)
        self.min_overall_score = self.config.get("min_overall_score", 0.75)

        # Required sections (can be overridden per-module)
        self.required_sections = self.config.get(
            "required_sections",
            self.DEFAULT_REQUIRED_SECTIONS
        )

    def evaluate(self, module: dict, doc_content: str) -> StructureResult:
        """
        Evaluate structure of documentation.

        Args:
            module: Module definition from modules.json
            doc_content: Content of the generated documentation

        Returns:
            StructureResult with scores and issues
        """
        issues = []

        # Get required sections (module-specific or default)
        required_sections = module.get("expected_sections", self.required_sections)

        # Check sections
        section_result = self._check_sections(doc_content, required_sections)

        # Check format elements
        has_mermaid = self._has_mermaid_diagram(doc_content)
        has_tables = self._has_tables(doc_content)
        has_code_blocks = self._has_code_blocks(doc_content)
        has_overview = self._has_overview(doc_content)

        # Quality metrics
        word_count = self._count_words(doc_content)
        heading_count = self._count_headings(doc_content)

        # Build issues list
        if section_result["missing"]:
            issues.append(f"Missing sections: {', '.join(section_result['missing'])}")

        if self.require_mermaid and not has_mermaid:
            issues.append("No Mermaid diagram found")

        if self.require_code_blocks and not has_code_blocks:
            issues.append("No code blocks found")

        if word_count < self.min_word_count:
            issues.append(f"Document too short: {word_count} words (min: {self.min_word_count})")

        if not has_overview:
            issues.append("Missing or empty Overview section")

        # Calculate score
        # Weights: sections (50%), format (30%), quality (20%)
        section_score = section_result["coverage"]

        format_score = self._calculate_format_score(
            has_mermaid, has_tables, has_code_blocks, has_overview
        )

        quality_score = self._calculate_quality_score(word_count, heading_count)

        overall_score = (
            section_score * 0.50 +
            format_score * 0.30 +
            quality_score * 0.20
        )

        # Determine if passed
        passed = (
            overall_score >= self.min_overall_score and
            section_result["coverage"] >= self.min_section_coverage and
            (not self.require_mermaid or has_mermaid) and
            (not self.require_code_blocks or has_code_blocks)
        )

        return StructureResult(
            score=overall_score,
            passed=passed,
            sections_found=section_result["found"],
            sections_missing=section_result["missing"],
            section_coverage=section_result["coverage"],
            has_mermaid_diagram=has_mermaid,
            has_tables=has_tables,
            has_code_blocks=has_code_blocks,
            has_overview=has_overview,
            word_count=word_count,
            heading_count=heading_count,
            issues=issues,
        )

    def _check_sections(self, doc_content: str, required_sections: list) -> dict:
        """Check if required sections are present."""
        found = []
        missing = []

        # Extract all headings from document
        headings = self._extract_headings(doc_content)
        headings_lower = [h.lower() for h in headings]

        for section in required_sections:
            section_lower = section.lower()

            # Check direct match
            if self._section_found(section_lower, headings_lower):
                found.append(section)
            else:
                missing.append(section)

        coverage = len(found) / len(required_sections) if required_sections else 1.0

        return {
            "found": found,
            "missing": missing,
            "coverage": coverage,
        }

    def _section_found(self, section: str, headings: list) -> bool:
        """Check if a section is found, considering aliases."""
        section_lower = section.lower()

        # Direct match
        if section_lower in headings:
            return True

        # Check aliases
        aliases = self.SECTION_ALIASES.get(section_lower, [section_lower])
        for alias in aliases:
            if alias in headings:
                return True
            # Partial match
            for heading in headings:
                if alias in heading or heading in alias:
                    return True

        return False

    def _extract_headings(self, doc_content: str) -> list:
        """Extract all markdown headings from document."""
        # Match ## Heading or # Heading
        pattern = r'^#{1,6}\s+(.+)$'
        matches = re.findall(pattern, doc_content, re.MULTILINE)
        return [m.strip() for m in matches]

    def _has_mermaid_diagram(self, doc_content: str) -> bool:
        """Check if document contains Mermaid diagrams."""
        patterns = [
            r'```mermaid',
            r'```\s*mermaid',
            r'graph\s+(TD|TB|BT|RL|LR)',
            r'sequenceDiagram',
            r'classDiagram',
            r'flowchart',
        ]
        for pattern in patterns:
            if re.search(pattern, doc_content, re.IGNORECASE):
                return True
        return False

    def _has_tables(self, doc_content: str) -> bool:
        """Check if document contains markdown tables."""
        # Look for table row pattern: | col1 | col2 |
        table_pattern = r'\|[^|]+\|[^|]+\|'
        return bool(re.search(table_pattern, doc_content))

    def _has_code_blocks(self, doc_content: str) -> bool:
        """Check if document contains code blocks."""
        # Look for ``` or indented code
        return '```' in doc_content

    def _has_overview(self, doc_content: str) -> bool:
        """Check if document has a non-empty overview section."""
        # Find overview section and check it has content
        pattern = r'##?\s*Overview\s*\n+([\s\S]*?)(?=\n##|\Z)'
        match = re.search(pattern, doc_content, re.IGNORECASE)

        if match:
            content = match.group(1).strip()
            # Check it has meaningful content (more than just whitespace)
            words = len(content.split())
            return words >= 10  # At least 10 words

        return False

    def _count_words(self, doc_content: str) -> int:
        """Count words in document (excluding code blocks)."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', doc_content)
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        # Count words
        words = text.split()
        return len(words)

    def _count_headings(self, doc_content: str) -> int:
        """Count number of headings."""
        return len(self._extract_headings(doc_content))

    def _calculate_format_score(
        self,
        has_mermaid: bool,
        has_tables: bool,
        has_code_blocks: bool,
        has_overview: bool
    ) -> float:
        """Calculate format score based on presence of format elements."""
        score = 0.0

        # Overview is most important (40%)
        if has_overview:
            score += 0.40

        # Code blocks important (30%)
        if has_code_blocks:
            score += 0.30

        # Tables helpful (15%)
        if has_tables:
            score += 0.15

        # Mermaid diagrams nice to have (15%)
        if has_mermaid:
            score += 0.15

        return score

    def _calculate_quality_score(self, word_count: int, heading_count: int) -> float:
        """Calculate quality score based on metrics."""
        score = 0.0

        # Word count (up to 60%)
        if word_count >= 1000:
            score += 0.60
        elif word_count >= 500:
            score += 0.45
        elif word_count >= 200:
            score += 0.30
        elif word_count >= 100:
            score += 0.15

        # Heading count indicates good structure (up to 40%)
        if heading_count >= 8:
            score += 0.40
        elif heading_count >= 5:
            score += 0.30
        elif heading_count >= 3:
            score += 0.20
        elif heading_count >= 1:
            score += 0.10

        return score


def main():
    """Test the structure checker with sample data."""
    import json

    # Sample module
    module = {
        "name": "Authentication",
        "expected_sections": ["Overview", "Architecture", "API Endpoints", "Data Models"],
    }

    # Sample doc content
    doc_content = """
# Authentication

## Overview

The Authentication module handles user login, logout, and token management.
It provides secure authentication using JWT tokens and supports session management.
This module is critical for securing access to all protected resources.

## Architecture

```mermaid
graph TD
    A[Client] --> B[Auth Controller]
    B --> C[Auth Service]
    C --> D[User Repository]
    C --> E[Token Service]
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/login | User login |
| POST | /auth/logout | User logout |

## Data Models

```go
type LoginRequest struct {
    Email    string `json:"email"`
    Password string `json:"password"`
}

type LoginResponse struct {
    AccessToken  string `json:"access_token"`
    RefreshToken string `json:"refresh_token"`
}
```

## Dependencies

- User Service
- Token Service
- Redis (session storage)
    """

    checker = StructureChecker()
    result = checker.evaluate(module, doc_content)

    print("Structure Result:")
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()

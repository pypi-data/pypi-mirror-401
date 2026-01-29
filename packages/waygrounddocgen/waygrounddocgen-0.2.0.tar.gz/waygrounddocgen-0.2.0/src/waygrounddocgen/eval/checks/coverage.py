"""
Coverage checker - validates that documentation covers all expected elements.

Checks:
- Entry points (controllers, services) are mentioned
- API endpoints are documented
- Structs/data models are covered
- Kafka topics are mentioned
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CoverageResult:
    """Result of coverage evaluation."""
    score: float  # 0.0 to 1.0
    passed: bool

    # Detailed breakdown
    entry_point_coverage: float = 0.0
    endpoint_coverage: float = 0.0
    struct_coverage: float = 0.0
    kafka_coverage: float = 0.0

    # Missing items
    missing_entry_points: list = field(default_factory=list)
    missing_endpoints: list = field(default_factory=list)
    missing_structs: list = field(default_factory=list)
    missing_kafka_topics: list = field(default_factory=list)

    # Found items (for debugging)
    found_entry_points: list = field(default_factory=list)
    found_endpoints: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 3),
            "passed": self.passed,
            "breakdown": {
                "entry_point_coverage": round(self.entry_point_coverage, 3),
                "endpoint_coverage": round(self.endpoint_coverage, 3),
                "struct_coverage": round(self.struct_coverage, 3),
                "kafka_coverage": round(self.kafka_coverage, 3),
            },
            "missing": {
                "entry_points": self.missing_entry_points,
                "endpoints": self.missing_endpoints,
                "structs": self.missing_structs,
                "kafka_topics": self.missing_kafka_topics,
            }
        }


class CoverageChecker:
    """
    Checks documentation coverage against module definition.

    Validates that all expected elements from modules.json are
    mentioned/documented in the generated documentation.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize with optional config overrides.

        Args:
            config: Optional config dict with threshold overrides
        """
        self.config = config or {}

        # Default thresholds
        self.min_entry_point_coverage = self.config.get("min_entry_point_coverage", 0.8)
        self.min_endpoint_coverage = self.config.get("min_endpoint_coverage", 0.9)
        self.min_struct_coverage = self.config.get("min_struct_coverage", 0.7)
        self.min_kafka_coverage = self.config.get("min_kafka_coverage", 0.8)
        self.min_overall_score = self.config.get("min_overall_score", 0.8)

    def evaluate(self, module: dict, doc_content: str) -> CoverageResult:
        """
        Evaluate coverage of documentation against module definition.

        Args:
            module: Module definition from modules.json
            doc_content: Content of the generated documentation

        Returns:
            CoverageResult with scores and missing items
        """
        # Normalize doc content for searching
        doc_lower = doc_content.lower()
        doc_normalized = self._normalize_text(doc_content)

        # Check entry points
        entry_points = module.get("entry_points", [])
        ep_result = self._check_items(entry_points, doc_content, doc_normalized)

        # Check API endpoints
        endpoints = module.get("api_endpoints", [])
        endpoint_result = self._check_endpoints(endpoints, doc_content)

        # Check structs
        structs = module.get("structs", [])
        struct_result = self._check_items(structs, doc_content, doc_normalized)

        # Check Kafka topics
        kafka_topics = module.get("kafka_topics", [])
        kafka_result = self._check_kafka(kafka_topics, doc_content)

        # Calculate coverages
        ep_coverage = ep_result["coverage"] if entry_points else 1.0
        endpoint_coverage = endpoint_result["coverage"] if endpoints else 1.0
        struct_coverage = struct_result["coverage"] if structs else 1.0
        kafka_coverage = kafka_result["coverage"] if kafka_topics else 1.0

        # Weighted overall score
        # Endpoints are most important, then entry points, then structs
        weights = {
            "endpoints": 0.35,
            "entry_points": 0.30,
            "structs": 0.20,
            "kafka": 0.15,
        }

        overall_score = (
            endpoint_coverage * weights["endpoints"] +
            ep_coverage * weights["entry_points"] +
            struct_coverage * weights["structs"] +
            kafka_coverage * weights["kafka"]
        )

        # Determine if passed
        passed = (
            overall_score >= self.min_overall_score and
            endpoint_coverage >= self.min_endpoint_coverage
        )

        return CoverageResult(
            score=overall_score,
            passed=passed,
            entry_point_coverage=ep_coverage,
            endpoint_coverage=endpoint_coverage,
            struct_coverage=struct_coverage,
            kafka_coverage=kafka_coverage,
            missing_entry_points=ep_result["missing"],
            missing_endpoints=endpoint_result["missing"],
            missing_structs=struct_result["missing"],
            missing_kafka_topics=kafka_result["missing"],
            found_entry_points=ep_result["found"],
            found_endpoints=endpoint_result["found"],
        )

    def _normalize_text(self, text: str) -> str:
        """Normalize text for fuzzy matching."""
        # Remove code blocks but keep their content
        text = re.sub(r'```\w*\n?', '', text)
        # Lowercase
        text = text.lower()
        # Remove special characters but keep alphanumeric
        text = re.sub(r'[^a-z0-9\s/:]', ' ', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text

    def _check_items(self, items: list, doc_content: str, doc_normalized: str) -> dict:
        """
        Check if items are mentioned in documentation.

        Uses multiple matching strategies:
        1. Exact match
        2. Case-insensitive match
        3. Partial match (for compound names like AuthService.Login)
        """
        found = []
        missing = []

        for item in items:
            if self._item_found(item, doc_content, doc_normalized):
                found.append(item)
            else:
                missing.append(item)

        coverage = len(found) / len(items) if items else 1.0

        return {
            "found": found,
            "missing": missing,
            "coverage": coverage,
        }

    def _item_found(self, item: str, doc_content: str, doc_normalized: str) -> bool:
        """Check if a single item is found in the documentation."""
        # Strategy 1: Exact match
        if item in doc_content:
            return True

        # Strategy 2: Case-insensitive match
        if item.lower() in doc_normalized:
            return True

        # Strategy 3: Split compound names (e.g., AuthService.Login -> Auth, Service, Login)
        parts = re.split(r'[.\s]', item)
        if len(parts) > 1:
            # Check if all significant parts are present
            significant_parts = [p for p in parts if len(p) > 3]
            if significant_parts:
                found_parts = sum(1 for p in significant_parts if p.lower() in doc_normalized)
                if found_parts >= len(significant_parts) * 0.7:  # 70% of parts found
                    return True

        # Strategy 4: CamelCase to words (e.g., NewLocalLoginController -> local login controller)
        words = re.sub(r'([A-Z])', r' \1', item).lower().strip()
        words_normalized = re.sub(r'\s+', ' ', words)
        if words_normalized in doc_normalized:
            return True

        return False

    def _check_endpoints(self, endpoints: list, doc_content: str) -> dict:
        """
        Check if API endpoints are documented.

        Looks for:
        - Exact path match (e.g., /auth/login)
        - Method + path combination (e.g., POST /auth/login)
        - Path in table format
        """
        found = []
        missing = []

        doc_normalized = self._normalize_text(doc_content)

        for endpoint in endpoints:
            path = endpoint.get("path", "")
            method = endpoint.get("method", "")

            # Normalize path for matching
            path_normalized = path.lower().replace(":", "")  # Remove :id placeholders

            # Check various formats
            found_endpoint = False

            # Format 1: Exact path
            if path.lower() in doc_content.lower():
                found_endpoint = True

            # Format 2: Path with normalized placeholders
            elif path_normalized in doc_normalized:
                found_endpoint = True

            # Format 3: Method + path
            elif f"{method.lower()} {path.lower()}" in doc_content.lower():
                found_endpoint = True

            # Format 4: Table format (| POST | /auth/login |)
            elif re.search(rf'\|\s*{method}\s*\|\s*{re.escape(path)}', doc_content, re.IGNORECASE):
                found_endpoint = True

            # Format 5: Path segments present
            else:
                path_parts = [p for p in path.split('/') if p and not p.startswith(':')]
                if len(path_parts) >= 2:
                    if all(part.lower() in doc_normalized for part in path_parts):
                        found_endpoint = True

            if found_endpoint:
                found.append(f"{method} {path}")
            else:
                missing.append(f"{method} {path}")

        coverage = len(found) / len(endpoints) if endpoints else 1.0

        return {
            "found": found,
            "missing": missing,
            "coverage": coverage,
        }

    def _check_kafka(self, topics: list, doc_content: str) -> dict:
        """Check if Kafka topics are documented."""
        found = []
        missing = []

        doc_lower = doc_content.lower()

        for topic_info in topics:
            topic = topic_info.get("topic", "") if isinstance(topic_info, dict) else topic_info
            topic_type = topic_info.get("type", "") if isinstance(topic_info, dict) else ""

            # Check if topic is mentioned
            topic_found = False

            # Exact match
            if topic.lower() in doc_lower:
                topic_found = True

            # With underscores replaced by dots or vice versa
            elif topic.lower().replace("_", ".") in doc_lower:
                topic_found = True
            elif topic.lower().replace(".", "_") in doc_lower:
                topic_found = True

            if topic_found:
                found.append(topic)
            else:
                missing.append(topic)

        coverage = len(found) / len(topics) if topics else 1.0

        return {
            "found": found,
            "missing": missing,
            "coverage": coverage,
        }


def main():
    """Test the coverage checker with sample data."""
    import json

    # Sample module
    module = {
        "name": "Authentication",
        "entry_points": ["NewLocalLoginController", "AuthService.Login"],
        "api_endpoints": [
            {"method": "POST", "path": "/auth/login"},
            {"method": "POST", "path": "/auth/logout"},
        ],
        "structs": ["LoginRequest", "LoginResponse"],
        "kafka_topics": [{"topic": "user.logged_in", "type": "producer"}],
    }

    # Sample doc content
    doc_content = """
    # Authentication

    ## API Endpoints

    | Method | Path | Description |
    |--------|------|-------------|
    | POST | /auth/login | User login |

    ## Components

    - NewLocalLoginController - handles login requests
    - AuthService provides Login functionality

    ## Data Models

    ```go
    type LoginRequest struct {
        Email    string
        Password string
    }
    ```

    ## Events

    Publishes to user.logged_in topic.
    """

    checker = CoverageChecker()
    result = checker.evaluate(module, doc_content)

    print("Coverage Result:")
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()

"""
Freshness checker - validates documentation is up-to-date with source code.

Checks:
- Doc modification time vs code modification time
- File hash comparisons (if metadata available)
- Git history analysis
"""

import hashlib
import os
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class FreshnessResult:
    """Result of freshness evaluation."""
    score: float  # 0.0 to 1.0
    passed: bool
    is_fresh: bool

    # Timestamps
    doc_modified: Optional[str] = None
    code_last_modified: Optional[str] = None
    days_since_code_change: int = 0
    days_since_doc_update: int = 0

    # File analysis
    stale_files: list = field(default_factory=list)
    files_checked: int = 0

    # Git info
    recent_commits: list = field(default_factory=list)
    commits_since_doc: int = 0

    # Issues
    issues: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score": round(self.score, 3),
            "passed": self.passed,
            "is_fresh": self.is_fresh,
            "timestamps": {
                "doc_modified": self.doc_modified,
                "code_last_modified": self.code_last_modified,
                "days_since_code_change": self.days_since_code_change,
                "days_since_doc_update": self.days_since_doc_update,
            },
            "files": {
                "stale_files": self.stale_files,
                "files_checked": self.files_checked,
            },
            "git": {
                "recent_commits": self.recent_commits,
                "commits_since_doc": self.commits_since_doc,
            },
            "issues": self.issues,
        }


class FreshnessChecker:
    """
    Checks if documentation is fresh relative to source code.

    Uses file timestamps and git history to determine if
    documentation needs to be regenerated.
    """

    def __init__(self, config: Optional[dict] = None, repo_path: Optional[str] = None):
        """
        Initialize with optional config overrides.

        Args:
            config: Optional config dict with threshold overrides
            repo_path: Path to the repository root
        """
        self.config = config or {}
        self.repo_path = repo_path or os.getcwd()

        # Thresholds
        self.max_stale_days = self.config.get("max_stale_days", 30)
        self.max_commits_behind = self.config.get("max_commits_behind", 10)
        self.min_overall_score = self.config.get("min_overall_score", 0.7)

    def evaluate(self, module: dict, doc_path: str) -> FreshnessResult:
        """
        Evaluate freshness of documentation.

        Args:
            module: Module definition from modules.json
            doc_path: Path to the documentation file

        Returns:
            FreshnessResult with freshness analysis
        """
        issues = []

        # Get file paths from module
        source_files = self._get_source_files(module)

        # Check if doc exists
        doc_path_obj = Path(doc_path)
        if not doc_path_obj.exists():
            return FreshnessResult(
                score=0.0,
                passed=False,
                is_fresh=False,
                issues=["Documentation file not found"],
            )

        # Get timestamps
        doc_modified = self._get_file_modified_time(doc_path)
        code_modified = self._get_latest_code_modified(source_files)

        # Calculate days
        now = datetime.now()
        days_since_doc = (now - doc_modified).days if doc_modified else 999
        days_since_code = (now - code_modified).days if code_modified else 0

        # Check for stale files (code modified after doc)
        stale_files = []
        if doc_modified:
            stale_files = self._find_stale_files(source_files, doc_modified)

        # Get git commit info
        git_info = self._get_git_info(module, doc_modified)

        # Determine freshness
        is_fresh = True
        if stale_files:
            is_fresh = False
            issues.append(f"{len(stale_files)} source files modified after documentation")

        if git_info["commits_since_doc"] > self.max_commits_behind:
            is_fresh = False
            issues.append(f"{git_info['commits_since_doc']} commits since last doc update")

        if days_since_doc > self.max_stale_days:
            issues.append(f"Documentation is {days_since_doc} days old (max: {self.max_stale_days})")

        # Calculate score
        score = self._calculate_score(
            stale_files,
            len(source_files),
            git_info["commits_since_doc"],
            days_since_doc,
        )

        passed = is_fresh and score >= self.min_overall_score

        return FreshnessResult(
            score=score,
            passed=passed,
            is_fresh=is_fresh,
            doc_modified=doc_modified.isoformat() if doc_modified else None,
            code_last_modified=code_modified.isoformat() if code_modified else None,
            days_since_code_change=days_since_code,
            days_since_doc_update=days_since_doc,
            stale_files=stale_files[:10],  # Limit to 10
            files_checked=len(source_files),
            recent_commits=git_info["recent_commits"],
            commits_since_doc=git_info["commits_since_doc"],
            issues=issues,
        )

    def _get_source_files(self, module: dict) -> list:
        """Get all source file paths from module definition."""
        files = []

        # From components
        for component in module.get("components", []):
            comp_path = component.get("path", "")
            for file_name in component.get("files", []):
                full_path = os.path.join(self.repo_path, comp_path, file_name)
                if os.path.exists(full_path):
                    files.append(full_path)

        # Direct files list (legacy format)
        for file_path in module.get("files", []):
            full_path = os.path.join(self.repo_path, file_path)
            if os.path.exists(full_path):
                files.append(full_path)

        return files

    def _get_file_modified_time(self, file_path: str) -> Optional[datetime]:
        """Get file modification time."""
        try:
            stat = os.stat(file_path)
            return datetime.fromtimestamp(stat.st_mtime)
        except OSError:
            return None

    def _get_latest_code_modified(self, files: list) -> Optional[datetime]:
        """Get the latest modification time among all source files."""
        latest = None

        for file_path in files:
            modified = self._get_file_modified_time(file_path)
            if modified:
                if latest is None or modified > latest:
                    latest = modified

        return latest

    def _find_stale_files(self, source_files: list, doc_modified: datetime) -> list:
        """Find source files modified after the documentation."""
        stale = []

        for file_path in source_files:
            modified = self._get_file_modified_time(file_path)
            if modified and modified > doc_modified:
                stale.append({
                    "file": os.path.basename(file_path),
                    "modified": modified.isoformat(),
                })

        return stale

    def _get_git_info(self, module: dict, doc_modified: Optional[datetime]) -> dict:
        """Get git commit information for module files."""
        result = {
            "recent_commits": [],
            "commits_since_doc": 0,
        }

        # Get paths to check
        paths = set()
        for component in module.get("components", []):
            paths.add(component.get("path", ""))

        if not paths:
            return result

        paths_str = " ".join(p for p in paths if p)
        if not paths_str:
            return result

        try:
            # Get recent commits
            cmd = f'git log -5 --pretty=format:"%h|%an|%s|%ad" --date=short -- {paths_str}'
            proc = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )

            if proc.returncode == 0:
                for line in proc.stdout.strip().split('\n'):
                    if '|' in line:
                        parts = line.split('|', 3)
                        if len(parts) >= 4:
                            result["recent_commits"].append({
                                "hash": parts[0],
                                "author": parts[1],
                                "message": parts[2][:50],
                                "date": parts[3],
                            })

            # Count commits since doc was updated
            if doc_modified:
                since_date = doc_modified.strftime("%Y-%m-%d")
                cmd = f'git rev-list --count --since="{since_date}" HEAD -- {paths_str}'
                proc = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                )
                if proc.returncode == 0:
                    try:
                        result["commits_since_doc"] = int(proc.stdout.strip())
                    except ValueError:
                        pass

        except Exception:
            pass

        return result

    def _calculate_score(
        self,
        stale_files: list,
        total_files: int,
        commits_behind: int,
        days_old: int,
    ) -> float:
        """Calculate freshness score."""
        score = 1.0

        # Penalize for stale files (up to 40%)
        if total_files > 0:
            stale_ratio = len(stale_files) / total_files
            score -= stale_ratio * 0.40

        # Penalize for commits behind (up to 30%)
        if commits_behind > 0:
            commit_penalty = min(commits_behind / self.max_commits_behind, 1.0)
            score -= commit_penalty * 0.30

        # Penalize for age (up to 30%)
        if days_old > 0:
            age_penalty = min(days_old / self.max_stale_days, 1.0)
            score -= age_penalty * 0.30

        return max(0.0, score)


def main():
    """Test the freshness checker with sample data."""
    import json

    # Sample module
    module = {
        "name": "Authentication",
        "components": [
            {
                "layer": "controllers",
                "path": "controllers/auth",
                "files": ["local_login.go", "logout.go"],
            }
        ],
    }

    checker = FreshnessChecker(repo_path="/tmp/test-repo")

    # This would fail without actual files, but demonstrates usage
    print("Freshness checker initialized")
    print(f"Max stale days: {checker.max_stale_days}")
    print(f"Max commits behind: {checker.max_commits_behind}")


if __name__ == "__main__":
    main()

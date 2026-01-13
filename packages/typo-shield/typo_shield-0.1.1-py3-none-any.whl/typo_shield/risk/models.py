"""
Risk finding models.

Data structures for representing security and quality findings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class RiskFinding:
    """
    Represents a security or quality finding.

    Attributes:
        kind: Type of finding (e.g., "typosquat", "missing_dep", "unknown")
        subject: What the finding is about ("dep" or "import")
        name: The package/module name
        target: For typosquat findings, the suspected target package
        level: Severity level (INFO, WARN, FAIL)
        code: Error code (e.g., "TS001", "TS101")
        message: Human-readable description
        file: Optional file path where the issue was found
        lineno: Optional line number
        context: Optional additional context information

    Examples:
        >>> # Typosquat finding
        >>> RiskFinding(
        ...     kind="typosquat",
        ...     subject="dep",
        ...     name="reqeusts",
        ...     target="requests",
        ...     level="FAIL",
        ...     code="TS001",
        ...     message="Suspected typosquat: 'reqeusts' is similar to 'requests'",
        ...     file="requirements.txt",
        ...     lineno=5,
        ... )

        >>> # Missing dependency finding
        >>> RiskFinding(
        ...     kind="missing_dep",
        ...     subject="import",
        ...     name="pandas",
        ...     target=None,
        ...     level="WARN",
        ...     code="TS101",
        ...     message="Import 'pandas' not found in declared dependencies",
        ...     file="src/main.py",
        ...     lineno=3,
        ... )
    """

    kind: str
    subject: Literal["dep", "import"]
    name: str
    target: str | None
    level: Literal["INFO", "WARN", "FAIL"]
    code: str
    message: str
    file: str | None = None
    lineno: int | None = None
    context: dict[str, str] | None = None

    def __str__(self) -> str:
        """String representation for terminal output."""
        location = ""
        if self.file:
            location = f" in {self.file}"
            if self.lineno:
                location += f":{self.lineno}"

        return f"[{self.level}] {self.code}: {self.message}{location}"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "kind": self.kind,
            "subject": self.subject,
            "name": self.name,
            "target": self.target,
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "file": self.file,
            "lineno": self.lineno,
            "context": self.context,
        }


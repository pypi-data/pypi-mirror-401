"""Simple keyword-based toxicity detector."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

# Try importing SAGE base classes
try:
    from sage.libs.safety.interface.base import (
        BaseToxicityDetector,
        SafetyAction,
        SafetyCategory,
        SafetyResult,
    )

    _HAS_SAGE = True
except ImportError:
    BaseToxicityDetector = object
    _HAS_SAGE = False

    class SafetyAction(Enum):
        ALLOW = "allow"
        WARN = "warn"
        BLOCK = "block"

    class SafetyCategory(Enum):
        TOXICITY = "toxicity"
        HATE_SPEECH = "hate_speech"
        VIOLENCE = "violence"

    @dataclass
    class SafetyResult:
        is_safe: bool
        action: SafetyAction = SafetyAction.ALLOW
        category: Optional[SafetyCategory] = None
        confidence: float = 0.0
        detected_issues: list[str] = field(default_factory=list)
        modified_content: Optional[str] = None
        metadata: dict[str, Any] = field(default_factory=dict)


# Default toxicity keywords (simplified - in production use ML models)
DEFAULT_TOXIC_PATTERNS = {
    SafetyCategory.HATE_SPEECH: [
        r"\bhateful\b",
        r"\bhate_marker\b",
    ],
    SafetyCategory.VIOLENCE: [
        r"\bkill\s+(?:you|them|him|her|all)\b",
        r"\bviolent\b",
    ],
    SafetyCategory.TOXICITY: [
        r"\btoxic\b",
        r"\bcustom_toxic\b",
    ],
}


class SimpleToxicityDetector(BaseToxicityDetector):
    """Simple keyword-based toxicity detector.

    For demonstration purposes. Production systems should use
    ML-based classifiers like Perspective API.

    Example:
        >>> detector = SimpleToxicityDetector()
        >>> result = detector.detect("This is normal text")
        >>> print(result.is_safe)
        True
    """

    def __init__(
        self,
        threshold: float = 0.5,
        custom_patterns: dict[SafetyCategory, list[str]] | None = None,
    ) -> None:
        """Initialize detector.

        Args:
            threshold: Score threshold for flagging content.
            custom_patterns: Custom patterns by category.
        """
        self._threshold = threshold
        self._patterns: dict[SafetyCategory, list[re.Pattern]] = {}

        # Compile default patterns
        for category, patterns in DEFAULT_TOXIC_PATTERNS.items():
            self._patterns[category] = [
                re.compile(p, re.IGNORECASE) for p in patterns
            ]

        # Add custom patterns
        if custom_patterns:
            for category, patterns in custom_patterns.items():
                if category not in self._patterns:
                    self._patterns[category] = []
                self._patterns[category].extend(
                    re.compile(p, re.IGNORECASE) for p in patterns
                )

    @property
    def name(self) -> str:
        """Return detector name."""
        return "simple_toxicity"

    def detect(
        self,
        text: str,
        **kwargs: Any,
    ) -> SafetyResult:
        """Detect toxicity in text.

        Args:
            text: Text to analyze.
            **kwargs: Additional arguments.

        Returns:
            SafetyResult with detection status.
        """
        scores: dict[str, float] = {}
        detected_issues: list[str] = []
        max_score = 0.0
        max_category: Optional[SafetyCategory] = None

        for category, patterns in self._patterns.items():
            match_count = 0
            for pattern in patterns:
                matches = pattern.findall(text)
                if matches:
                    match_count += len(matches)
                    detected_issues.append(
                        f"{category.value}: {matches[0][:30]}..."
                    )

            # Simple scoring: any match = 0.7, more matches = higher
            score = min(1.0, 0.7 + match_count * 0.1) if match_count > 0 else 0.0
            scores[category.value] = score

            if score > max_score:
                max_score = score
                max_category = category

        is_safe = max_score < self._threshold

        return SafetyResult(
            is_safe=is_safe,
            action=SafetyAction.ALLOW if is_safe else SafetyAction.BLOCK,
            category=max_category,
            confidence=1.0 - max_score if is_safe else max_score,
            detected_issues=detected_issues,
            metadata={"scores": scores},
        )

    def get_scores(
        self,
        text: str,
        **kwargs: Any,
    ) -> dict[str, float]:
        """Get detailed toxicity scores by category.

        Args:
            text: Text to analyze.
            **kwargs: Additional arguments.

        Returns:
            Dictionary mapping categories to scores.
        """
        result = self.detect(text, **kwargs)
        return result.metadata.get("scores", {})

    def add_pattern(
        self,
        pattern: str,
        category: SafetyCategory = SafetyCategory.TOXICITY,
    ) -> None:
        """Add a custom toxicity pattern.

        Args:
            pattern: Regex pattern.
            category: Toxicity category.
        """
        if category not in self._patterns:
            self._patterns[category] = []
        self._patterns[category].append(re.compile(pattern, re.IGNORECASE))

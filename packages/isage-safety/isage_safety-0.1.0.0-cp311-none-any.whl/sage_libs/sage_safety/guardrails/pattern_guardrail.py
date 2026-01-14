"""Pattern-based content guardrail."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# Try importing SAGE base classes
try:
    from sage.libs.safety.interface.base import (
        BaseGuardrail,
        SafetyAction,
        SafetyCategory,
        SafetyResult,
    )

    _HAS_SAGE = True
except ImportError:
    # Define minimal local types
    BaseGuardrail = object
    _HAS_SAGE = False

    class SafetyAction(Enum):
        ALLOW = "allow"
        WARN = "warn"
        MODIFY = "modify"
        BLOCK = "block"

    class SafetyCategory(Enum):
        TOXICITY = "toxicity"
        HATE_SPEECH = "hate_speech"
        VIOLENCE = "violence"
        CUSTOM = "custom"

    @dataclass
    class SafetyResult:
        is_safe: bool
        action: SafetyAction = SafetyAction.ALLOW
        category: SafetyCategory | None = None
        confidence: float = 0.0
        detected_issues: list[str] = field(default_factory=list)
        modified_content: str | None = None
        metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PatternRule:
    """A pattern rule for content checking."""

    pattern: str
    category: SafetyCategory
    action: SafetyAction = SafetyAction.BLOCK
    description: str = ""
    case_sensitive: bool = False


class PatternGuardrail(BaseGuardrail):
    """Pattern-based content safety guardrail.

    Uses regex patterns to detect unsafe content.

    Example:
        >>> guardrail = PatternGuardrail()
        >>> guardrail.add_pattern(r"badword", SafetyCategory.TOXICITY)
        >>> result = guardrail.check("This contains badword")
        >>> print(result.is_safe)
        False
    """

    def __init__(
        self,
        rules: list[PatternRule] | None = None,
        default_action: SafetyAction = SafetyAction.BLOCK,
    ) -> None:
        """Initialize pattern guardrail.

        Args:
            rules: Initial list of pattern rules.
            default_action: Default action when patterns match.
        """
        self._rules: list[PatternRule] = rules or []
        self._default_action = default_action
        self._compiled_patterns: list[tuple[re.Pattern, PatternRule]] = []
        self._compile_patterns()

    @property
    def name(self) -> str:
        """Return guardrail name."""
        return "pattern"

    @property
    def categories(self) -> list[SafetyCategory]:
        """Return handled categories."""
        return list({rule.category for rule in self._rules}) or [SafetyCategory.CUSTOM]

    def _compile_patterns(self) -> None:
        """Compile all patterns."""
        self._compiled_patterns = []
        for rule in self._rules:
            flags = 0 if rule.case_sensitive else re.IGNORECASE
            compiled = re.compile(rule.pattern, flags)
            self._compiled_patterns.append((compiled, rule))

    def add_pattern(
        self,
        pattern: str,
        category: SafetyCategory = SafetyCategory.CUSTOM,
        action: SafetyAction | None = None,
        description: str = "",
        case_sensitive: bool = False,
    ) -> None:
        """Add a pattern rule.

        Args:
            pattern: Regex pattern string.
            category: Safety category.
            action: Action to take on match.
            description: Description of the pattern.
            case_sensitive: Whether pattern is case sensitive.
        """
        rule = PatternRule(
            pattern=pattern,
            category=category,
            action=action or self._default_action,
            description=description,
            case_sensitive=case_sensitive,
        )
        self._rules.append(rule)
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled = re.compile(pattern, flags)
        self._compiled_patterns.append((compiled, rule))

    def add_blocklist(
        self,
        words: list[str],
        category: SafetyCategory = SafetyCategory.TOXICITY,
        action: SafetyAction = SafetyAction.BLOCK,
    ) -> None:
        """Add a list of blocked words.

        Args:
            words: List of words to block.
            category: Category for all words.
            action: Action to take.
        """
        for word in words:
            # Word boundary pattern
            pattern = rf"\b{re.escape(word)}\b"
            self.add_pattern(pattern, category, action, f"Blocklist word: {word}")

    def check(
        self,
        content: str,
        context: str | None = None,
        **kwargs: Any,
    ) -> SafetyResult:
        """Check content against patterns.

        Args:
            content: Content to check.
            context: Optional context (unused).
            **kwargs: Additional arguments.

        Returns:
            SafetyResult with detection status.
        """
        detected_issues: list[str] = []
        matched_rules: list[PatternRule] = []

        for compiled, rule in self._compiled_patterns:
            matches = compiled.findall(content)
            if matches:
                detected_issues.append(f"Pattern '{rule.pattern}' matched: {matches[:3]}")
                matched_rules.append(rule)

        if not matched_rules:
            return SafetyResult(
                is_safe=True,
                action=SafetyAction.ALLOW,
                confidence=1.0,
                detected_issues=[],
                metadata={"patterns_checked": len(self._compiled_patterns)},
            )

        # Determine most severe action
        action_priority = {
            SafetyAction.BLOCK: 4,
            SafetyAction.MODIFY: 3,
            SafetyAction.WARN: 2,
            SafetyAction.ALLOW: 1,
        }
        most_severe = max(matched_rules, key=lambda r: action_priority.get(r.action, 0))

        return SafetyResult(
            is_safe=False,
            action=most_severe.action,
            category=most_severe.category,
            confidence=1.0,  # Pattern match is binary
            detected_issues=detected_issues,
            metadata={
                "patterns_checked": len(self._compiled_patterns),
                "patterns_matched": len(matched_rules),
            },
        )

    def filter(
        self,
        content: str,
        replacement: str = "[REDACTED]",
        **kwargs: Any,
    ) -> tuple[str, SafetyResult]:
        """Filter content by replacing matched patterns.

        Args:
            content: Content to filter.
            replacement: Replacement text.
            **kwargs: Additional arguments.

        Returns:
            Tuple of (filtered_content, SafetyResult).
        """
        filtered = content
        matches_count = 0

        for compiled, _rule in self._compiled_patterns:
            filtered, count = compiled.subn(replacement, filtered)
            matches_count += count

        is_safe = matches_count == 0
        result = SafetyResult(
            is_safe=is_safe,
            action=SafetyAction.ALLOW if is_safe else SafetyAction.MODIFY,
            confidence=1.0,
            detected_issues=[f"Replaced {matches_count} matches"] if matches_count > 0 else [],
            modified_content=filtered if matches_count > 0 else None,
            metadata={"replacements": matches_count},
        )

        return filtered, result

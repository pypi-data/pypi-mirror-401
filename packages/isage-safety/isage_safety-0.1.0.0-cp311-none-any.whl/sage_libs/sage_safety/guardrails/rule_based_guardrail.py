"""Rule-based content guardrail."""

from __future__ import annotations

from collections.abc import Callable
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
    BaseGuardrail = object
    _HAS_SAGE = False

    class SafetyAction(Enum):
        ALLOW = "allow"
        WARN = "warn"
        MODIFY = "modify"
        BLOCK = "block"

    class SafetyCategory(Enum):
        TOXICITY = "toxicity"
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


# Type for rule functions
RuleFunc = Callable[[str, str | None], tuple[bool, str]]


@dataclass
class ContentRule:
    """A content checking rule."""

    name: str
    check_func: RuleFunc
    category: SafetyCategory
    action: SafetyAction = SafetyAction.BLOCK
    description: str = ""


class RuleBasedGuardrail(BaseGuardrail):
    """Rule-based content safety guardrail.

    Uses custom rule functions to check content.

    Example:
        >>> def check_length(content, ctx):
        ...     if len(content) > 1000:
        ...         return False, "Content too long"
        ...     return True, ""
        >>> guardrail = RuleBasedGuardrail()
        >>> guardrail.add_rule("length_check", check_length)
        >>> result = guardrail.check("x" * 2000)
        >>> print(result.is_safe)
        False
    """

    def __init__(self) -> None:
        """Initialize rule-based guardrail."""
        self._rules: list[ContentRule] = []

    @property
    def name(self) -> str:
        """Return guardrail name."""
        return "rule_based"

    @property
    def categories(self) -> list[SafetyCategory]:
        """Return handled categories."""
        return list({rule.category for rule in self._rules}) or [SafetyCategory.CUSTOM]

    def add_rule(
        self,
        name: str,
        check_func: RuleFunc,
        category: SafetyCategory = SafetyCategory.CUSTOM,
        action: SafetyAction = SafetyAction.BLOCK,
        description: str = "",
    ) -> None:
        """Add a custom rule.

        Args:
            name: Rule name.
            check_func: Function(content, context) -> (is_safe, message).
            category: Safety category.
            action: Action to take on violation.
            description: Rule description.
        """
        rule = ContentRule(
            name=name,
            check_func=check_func,
            category=category,
            action=action,
            description=description,
        )
        self._rules.append(rule)

    def add_length_rule(
        self,
        max_length: int,
        action: SafetyAction = SafetyAction.BLOCK,
    ) -> None:
        """Add a content length rule.

        Args:
            max_length: Maximum allowed length.
            action: Action on violation.
        """

        def check_length(content: str, context: str | None) -> tuple[bool, str]:
            if len(content) > max_length:
                return False, f"Content exceeds {max_length} characters"
            return True, ""

        self.add_rule(
            f"max_length_{max_length}",
            check_length,
            SafetyCategory.CUSTOM,
            action,
            f"Maximum content length: {max_length}",
        )

    def add_word_count_rule(
        self,
        max_words: int,
        action: SafetyAction = SafetyAction.WARN,
    ) -> None:
        """Add a word count rule.

        Args:
            max_words: Maximum allowed words.
            action: Action on violation.
        """

        def check_words(content: str, context: str | None) -> tuple[bool, str]:
            word_count = len(content.split())
            if word_count > max_words:
                return False, f"Content has {word_count} words, max is {max_words}"
            return True, ""

        self.add_rule(
            f"max_words_{max_words}",
            check_words,
            SafetyCategory.CUSTOM,
            action,
            f"Maximum word count: {max_words}",
        )

    def add_required_keywords_rule(
        self,
        keywords: list[str],
        action: SafetyAction = SafetyAction.WARN,
    ) -> None:
        """Add a required keywords rule.

        Args:
            keywords: Keywords that must be present.
            action: Action on violation.
        """

        def check_keywords(content: str, context: str | None) -> tuple[bool, str]:
            content_lower = content.lower()
            missing = [kw for kw in keywords if kw.lower() not in content_lower]
            if missing:
                return False, f"Missing required keywords: {missing}"
            return True, ""

        self.add_rule(
            "required_keywords",
            check_keywords,
            SafetyCategory.CUSTOM,
            action,
            f"Required keywords: {keywords}",
        )

    def check(
        self,
        content: str,
        context: str | None = None,
        **kwargs: Any,
    ) -> SafetyResult:
        """Check content against all rules.

        Args:
            content: Content to check.
            context: Optional context.
            **kwargs: Additional arguments.

        Returns:
            SafetyResult with detection status.
        """
        detected_issues: list[str] = []
        violated_rules: list[ContentRule] = []

        for rule in self._rules:
            is_safe, message = rule.check_func(content, context)
            if not is_safe:
                detected_issues.append(f"Rule '{rule.name}': {message}")
                violated_rules.append(rule)

        if not violated_rules:
            return SafetyResult(
                is_safe=True,
                action=SafetyAction.ALLOW,
                confidence=1.0,
                detected_issues=[],
                metadata={"rules_checked": len(self._rules)},
            )

        # Determine most severe action
        action_priority = {
            SafetyAction.BLOCK: 4,
            SafetyAction.MODIFY: 3,
            SafetyAction.WARN: 2,
            SafetyAction.ALLOW: 1,
        }
        most_severe = max(violated_rules, key=lambda r: action_priority.get(r.action, 0))

        return SafetyResult(
            is_safe=False,
            action=most_severe.action,
            category=most_severe.category,
            confidence=1.0,
            detected_issues=detected_issues,
            metadata={
                "rules_checked": len(self._rules),
                "rules_violated": len(violated_rules),
            },
        )

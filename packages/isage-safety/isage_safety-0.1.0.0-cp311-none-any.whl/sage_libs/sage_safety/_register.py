"""Auto-register sage-safety components to SAGE interface."""

from __future__ import annotations

_REGISTERED = False


def register_to_sage() -> bool:
    """Register all safety components to SAGE.

    Returns:
        True if registration successful, False otherwise.
    """
    global _REGISTERED
    if _REGISTERED:
        return True

    try:
        from sage.libs.safety.interface import registry

        from sage_libs.sage_safety.detectors import (
            KeywordJailbreakDetector,
            SimpleToxicityDetector,
        )
        from sage_libs.sage_safety.guardrails import PatternGuardrail, RuleBasedGuardrail

        # Register guardrails
        registry.register("pattern", PatternGuardrail)
        registry.register("rule_based", RuleBasedGuardrail)

        # Register detectors
        registry.register("keyword_jailbreak", KeywordJailbreakDetector)
        registry.register("simple_toxicity", SimpleToxicityDetector)

        _REGISTERED = True
        return True
    except ImportError:
        # SAGE not installed - standalone mode
        return False
    except Exception:
        return False


def is_registered() -> bool:
    """Check if components are registered to SAGE."""
    return _REGISTERED

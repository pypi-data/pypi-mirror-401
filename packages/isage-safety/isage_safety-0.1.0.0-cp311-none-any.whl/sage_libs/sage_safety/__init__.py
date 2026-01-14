"""SAGE Safety - Safety and guardrails implementations.

This package provides safety and guardrails implementations:

Guardrails:
- PatternGuardrail: Pattern-based content filtering
- RuleBasedGuardrail: Rule-based content moderation

Detectors:
- KeywordJailbreakDetector: Keyword-based jailbreak detection
- SimpleToxicityDetector: Simple toxicity detection

Example:
    >>> from sage_safety import PatternGuardrail, KeywordJailbreakDetector
    >>> guardrail = PatternGuardrail()
    >>> result = guardrail.check("Some content to check")
    >>> print(result.is_safe)
    True
"""

# Auto-register to SAGE if available
from sage_libs.sage_safety._register import is_registered, register_to_sage
from sage_libs.sage_safety._version import __author__, __email__, __version__
from sage_libs.sage_safety.detectors import KeywordJailbreakDetector, SimpleToxicityDetector
from sage_libs.sage_safety.guardrails import PatternGuardrail, RuleBasedGuardrail

register_to_sage()

__all__ = [
    # Version
    "__version__",
    "__author__",
    "__email__",
    # Guardrails
    "PatternGuardrail",
    "RuleBasedGuardrail",
    # Detectors
    "KeywordJailbreakDetector",
    "SimpleToxicityDetector",
    # Registration
    "register_to_sage",
    "is_registered",
]

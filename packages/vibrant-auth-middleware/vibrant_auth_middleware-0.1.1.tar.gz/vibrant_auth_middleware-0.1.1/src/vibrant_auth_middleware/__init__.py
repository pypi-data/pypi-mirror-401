"""Vibrant Auth Middleware package."""

from .config import SigningMaterial
from .decisions import AuthDecision, allow, deny, error, decision_to_response_body
from .middleware import MiddlewareSettings, VibrantAuthMiddleware
from .telemetry import emit_decision_log
from .token_source import TokenOrigin, TokenSource, extract_token

__version__ = "2.0.0"

__all__ = [
    # Middleware
    "VibrantAuthMiddleware",
    "MiddlewareSettings",
    # Decisions
    "AuthDecision",
    "allow",
    "deny",
    "error",
    "decision_to_response_body",
    # Token extraction
    "TokenSource",
    "TokenOrigin",
    "extract_token",
    # Configuration
    "SigningMaterial",
    # Telemetry
    "emit_decision_log",
    # Version
    "__version__",
]

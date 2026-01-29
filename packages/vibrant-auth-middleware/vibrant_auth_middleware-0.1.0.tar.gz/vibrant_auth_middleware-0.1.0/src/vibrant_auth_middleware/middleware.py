"""FastAPI middleware for JWT extraction and verification."""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from fastapi import Request
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError
from starlette.datastructures import Headers
from starlette.responses import JSONResponse, Response

from . import config as config_module
from . import decisions as decisions_module
from . import telemetry as telemetry_module
from .decisions import AuthDecision
from .token_source import TokenSource, extract_token

if TYPE_CHECKING:  # pragma: no cover
    from .config import SigningMaterial
else:  # pragma: no cover - runtime alias for type hints
    SigningMaterial = Any

LOGGER = logging.getLogger("vibrant_auth.middleware")


@dataclass
class MiddlewareSettings:
    """
    Runtime configuration for authentication middleware.

    signing_material is required and must be valid.
    """
    signing_material: SigningMaterial  # Required: Direct material (no URL fetching)
    clock_skew_leeway: int = 30  # JWT exp/nbf clock tolerance in seconds


class VibrantAuthMiddleware:
    """Middleware that enforces JWT authentication with default-deny posture."""

    def __init__(self, app: Callable[..., Any], settings: MiddlewareSettings) -> None:
        """
        Initialize middleware with signing material.

        Args:
            app: ASGI application
            settings: Configuration including signing material (required)

        Raises:
            TypeError: If settings is not MiddlewareSettings instance
            ValueError: If signing_material is missing or invalid
        """
        self.app = app

        # Validate settings immediately (fail-fast)
        if not isinstance(settings, MiddlewareSettings):
            raise TypeError("settings must be MiddlewareSettings instance")

        config_module._validate_signing_material(settings.signing_material)

        self.settings = settings
        self._material: SigningMaterial = settings.signing_material  # Direct assignment

    async def __call__(self, scope: Dict[str, Any], receive: Callable[..., Any], send: Callable[..., Any]) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        correlation_id = self._derive_correlation_id(scope)

        try:
            token_source = extract_token(request)
            correlation_id = token_source.correlation_id or correlation_id
        except ValueError as extraction_error:
            reason = str(extraction_error) or "invalid_token"
            decision = decisions_module.deny(reason)
            await self._finalize_denied_request(scope, receive, send, decision, None, correlation_id)
            return

        material = self._material

        try:
            claims = decisions_module.verify_token(
                token_source.token,
                material,
                leeway=self.settings.clock_skew_leeway,
            )
            decision = decisions_module.allow(claims)
        except ExpiredSignatureError:
            decision = decisions_module.deny("token_expired")
        except DecodeError:
            decision = decisions_module.error("malformed_token")
        except InvalidTokenError as invalid:
            decision = decisions_module.deny(str(invalid) or "invalid_token")
        except ValueError as value_error:
            reason = str(value_error) or "invalid_token"
            decision = decisions_module.deny(reason)
        except Exception as exc:  # pragma: no cover - unexpected failure
            LOGGER.exception("unexpected verification error", exc_info=exc)
            decision = decisions_module.error("verification_error")

        if decision.status != "allow":
            await self._finalize_denied_request(scope, receive, send, decision, token_source, correlation_id)
            return

        self._attach_request_state(scope, decision, token_source, correlation_id, material)
        self._emit_telemetry(decision, token_source, correlation_id, material)
        await self.app(scope, receive, send)

    async def _finalize_denied_request(
        self,
        scope: Dict[str, Any],
        receive: Callable[..., Any],
        send: Callable[..., Any],
        decision: AuthDecision,
        token_source: Optional[TokenSource],
        correlation_id: str,
    ) -> None:
        self._attach_request_state(scope, decision, token_source, correlation_id, self._material)
        self._emit_telemetry(decision, token_source, correlation_id, self._material)
        response = self._render_response(decision, correlation_id)
        await response(scope, receive, send)

    def _attach_request_state(
        self,
        scope: Dict[str, Any],
        decision: AuthDecision,
        token_source: Optional[TokenSource],
        correlation_id: str,
        material: Optional[SigningMaterial],
    ) -> None:
        state = scope.setdefault("state", {})
        state["auth_decision"] = decision
        state["auth_claims"] = decision.claims
        state["correlation_id"] = correlation_id
        if token_source is not None:
            state["token_source"] = token_source.origin.value
        if material is not None:
            state["signing_material_version"] = material.version

    def _emit_telemetry(
        self,
        decision: AuthDecision,
        token_source: Optional[TokenSource],
        correlation_id: str,
        material: Optional[SigningMaterial],
    ) -> None:
        fields = {
            "decision": decision.status,
            "reason": decision.reason,
            "correlation_id": correlation_id,
            "principal": decision.principal,
            "token_source": token_source.origin.value if token_source else None,
        }
        if material is not None:
            fields["signing_material_version"] = material.version
        if decision.status == "allow":
            fields["claims"] = decision.claims
        telemetry_module.emit_decision_log(fields)

    @staticmethod
    def _derive_correlation_id(scope: Dict[str, Any]) -> str:
        headers = Headers(scope=scope)
        for header in ("x-correlation-id", "x-request-id"):
            value = headers.get(header)
            if value:
                return value
        return uuid.uuid4().hex

    @staticmethod
    def _render_response(decision: AuthDecision, correlation_id: str) -> Response:
        status_map = {"deny": 403, "error": 500, "allow": 200}
        detail_map = {
            "deny": "Access denied",
            "error": "Authentication service error",
            "allow": "OK",
        }
        body = {
            "detail": detail_map.get(decision.status, "Access denied"),
            "decision": decision.status,
            "reason": decision.reason,
            "correlation_id": correlation_id,
        }
        return JSONResponse(
            status_code=status_map.get(decision.status, 403),
            content=body,
        )

"""Integration coverage for negative authentication paths."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import jwt
import pytest
from fastapi import FastAPI, Request
from httpx import ASGITransport, AsyncClient

from vibrant_auth_middleware import MiddlewareSettings, VibrantAuthMiddleware
import vibrant_auth_middleware.config as config_module
from vibrant_auth_middleware.config import SigningMaterial
import vibrant_auth_middleware.decisions as decisions_module
import vibrant_auth_middleware.telemetry as telemetry_module


@dataclass
class NegativeScenario:
    name: str
    cookies: Dict[str, str]
    headers: Dict[str, str]
    expected_status: int
    expected_decision: str
    expected_reason: str
    verify_exception: Optional[Exception] = None


class NegativeTestHarness:
    """Provides deterministic responses for negative path testing."""

    def __init__(self) -> None:
        self.material = SigningMaterial(
            hs256_secret="neg-secret",
            rs256_public_keys={"test-key": "-----BEGIN PUBLIC KEY-----\ntest"},
            version="v1",
        )
        self.verify_calls: list[str] = []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "scenario",
    [
        NegativeScenario(
            name="missing_token_type",
            cookies={"access_token": "cookie-missing-type"},
            headers={},
            expected_status=403,
            expected_decision="deny",
            expected_reason="missing_token_type",
        ),
        NegativeScenario(
            name="expired_cookie",
            cookies={"access_token": "cookie-expired", "token_type": "Bearer"},
            headers={},
            expected_status=403,
            expected_decision="deny",
            expected_reason="token_expired",
            verify_exception=jwt.ExpiredSignatureError("expired"),
        ),
        NegativeScenario(
            name="malformed_header",
            cookies={},
            headers={"Authorization": "Bearer malformed"},
            expected_status=500,
            expected_decision="error",
            expected_reason="malformed_token",
            verify_exception=jwt.DecodeError("bad token"),
        ),
    ],
    ids=lambda scenario: scenario.name,
)
async def test_negative_auth_paths(monkeypatch, scenario: NegativeScenario) -> None:
    harness = NegativeTestHarness()

    def verify_token(token: str, signing_material: SigningMaterial, leeway: int = 30) -> Dict[str, Any]:
        harness.verify_calls.append(token)
        if scenario.verify_exception is not None:
            raise scenario.verify_exception
        return {"sub": "user", "ver": signing_material.version}

    monkeypatch.setattr(decisions_module, "verify_token", verify_token)
    monkeypatch.setattr(telemetry_module, "emit_decision_log", lambda _: None)

    app = FastAPI()

    @app.get("/protected")
    async def protected(request: Request) -> Dict[str, Any]:
        decision = getattr(request.state, "auth_decision", None)
        return {
            "decision": getattr(decision, "status", "missing"),
            "reason": getattr(decision, "reason", "missing"),
        }

    app.add_middleware(
        VibrantAuthMiddleware,
        settings=MiddlewareSettings(
            signing_material=harness.material,
            clock_skew_leeway=30,
        ),
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/protected", headers=scenario.headers, cookies=scenario.cookies)

    assert response.status_code == scenario.expected_status
    body = response.json()
    assert body["decision"] == scenario.expected_decision
    assert body["reason"] == scenario.expected_reason

    if scenario.name == "missing_token_type":
        assert harness.verify_calls == []
    else:
        assert harness.verify_calls != []


# ===== New Integration Tests for Updated Behavior (T010-T011) =====


@pytest.mark.asyncio
async def test_initialization_without_bootstrap_delay():
    """
    T010: Middleware is immediately ready after initialization (no async bootstrap).
    Reference: contracts/initialization-contract.md
    """
    app = FastAPI()

    material = SigningMaterial(
        hs256_secret="test-secret-immediate",
        rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
        version="immediate-1.0"
    )
    settings = MiddlewareSettings(signing_material=material)

    # Create middleware - should be immediately ready
    middleware = VibrantAuthMiddleware(app, settings)

    # Material should be available immediately (no async bootstrap)
    assert middleware._material == material
    assert middleware._material.version == "immediate-1.0"

    # Should not have any bootstrap-related state
    assert not hasattr(middleware, '_material_ready') or middleware._material_ready is None
    assert not hasattr(middleware, '_bootstrap_lock') or middleware._bootstrap_lock is None


def test_immutable_material():
    """
    T011: Attempt to modify material after initialization fails (frozen dataclass).
    Reference: contracts/initialization-contract.md
    """
    material = SigningMaterial(
        hs256_secret="test-secret",
        rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
        version="1.0"
    )

    # Attempt to modify material after creation should fail
    with pytest.raises((AttributeError, Exception)):
        material.version = "2.0"  # Should fail on frozen dataclass

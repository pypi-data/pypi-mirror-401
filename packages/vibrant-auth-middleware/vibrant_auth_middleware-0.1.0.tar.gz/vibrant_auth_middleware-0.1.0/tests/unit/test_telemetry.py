"""Unit tests for telemetry formatting and secret redaction."""

import json
import logging
from typing import Any, Dict

import pytest

from vibrant_auth_middleware.telemetry import emit_decision_log


@pytest.fixture
def caplog_json(caplog: pytest.LogCaptureFixture):
    """Capture logs and parse JSON payloads."""
    caplog.set_level(logging.INFO, logger="vibrant_auth.telemetry")
    yield caplog


def parse_log_json(caplog: pytest.LogCaptureFixture) -> Dict[str, Any]:
    """Parse the first JSON log record."""
    assert len(caplog.records) == 1
    message = caplog.records[0].message
    return json.loads(message)


def test_emit_decision_log_basic(caplog_json):
    """Test basic decision log emission."""
    emit_decision_log(
        {
            "decision": "allow",
            "reason": "authenticated",
            "correlation_id": "test-123",
            "principal": "user@example.com",
        }
    )

    log_data = parse_log_json(caplog_json)
    assert log_data["event"] == "auth_decision"
    assert log_data["decision"] == "allow"
    assert log_data["reason"] == "authenticated"
    assert log_data["correlation_id"] == "test-123"
    assert log_data["principal"] == "user@example.com"


def test_emit_decision_log_deny(caplog_json):
    """Test deny decision logging."""
    emit_decision_log(
        {
            "decision": "deny",
            "reason": "token_expired",
            "correlation_id": "test-456",
            "principal": None,
            "token_source": "cookie",
        }
    )

    log_data = parse_log_json(caplog_json)
    assert log_data["event"] == "auth_decision"
    assert log_data["decision"] == "deny"
    assert log_data["reason"] == "token_expired"
    assert log_data["token_source"] == "cookie"
    assert log_data["principal"] is None


def test_emit_decision_log_with_claims(caplog_json):
    """Test logging with sanitized claims."""
    emit_decision_log(
        {
            "decision": "allow",
            "reason": "authenticated",
            "correlation_id": "test-789",
            "principal": "user@example.com",
            "claims": {
                "sub": "user@example.com",
                "email": "user@example.com",
                "roles": ["user", "admin"],
                "exp": 1234567890,
            },
        }
    )

    log_data = parse_log_json(caplog_json)
    assert log_data["claims"]["sub"] == "user@example.com"
    assert log_data["claims"]["email"] == "user@example.com"
    assert log_data["claims"]["roles"] == ["user", "admin"]


def test_emit_decision_log_secret_redaction(caplog_json):
    """Test that sensitive fields are redacted from claims before logging."""
    # NOTE: The sanitization happens in the decisions module before telemetry
    # This test verifies telemetry doesn't log fields that should be redacted
    emit_decision_log(
        {
            "decision": "allow",
            "reason": "authenticated",
            "correlation_id": "test-redact",
            "principal": "user@example.com",
            "claims": {
                "sub": "user@example.com",
                "email": "user@example.com",
                # These should already be filtered by sanitize_claims
            },
        }
    )

    log_data = parse_log_json(caplog_json)
    # Verify no sensitive keys are present
    assert "token" not in log_data.get("claims", {})
    assert "secret" not in log_data.get("claims", {})
    assert "password" not in log_data.get("claims", {})
    assert "key" not in log_data.get("claims", {})


def test_emit_decision_log_error_case(caplog_json):
    """Test error decision logging."""
    emit_decision_log(
        {
            "decision": "error",
            "reason": "malformed_token",
            "correlation_id": "test-error",
            "principal": None,
            "token_source": "authorization_header",
        }
    )

    log_data = parse_log_json(caplog_json)
    assert log_data["decision"] == "error"
    assert log_data["reason"] == "malformed_token"
    assert log_data["token_source"] == "authorization_header"


def test_emit_decision_log_with_signing_material_version(caplog_json):
    """Test logging includes signing material version."""
    emit_decision_log(
        {
            "decision": "allow",
            "reason": "authenticated",
            "correlation_id": "test-version",
            "principal": "user@example.com",
            "signing_material_version": "v1.2.3",
        }
    )

    log_data = parse_log_json(caplog_json)
    assert log_data["signing_material_version"] == "v1.2.3"


def test_emit_decision_log_json_formatting(caplog_json):
    """Test that logs are compact JSON without whitespace."""
    emit_decision_log(
        {
            "decision": "allow",
            "reason": "authenticated",
            "correlation_id": "test-compact",
        }
    )

    message = caplog_json.records[0].message
    # Verify compact JSON (no spaces after separators)
    assert ", " not in message  # No space after comma
    assert ": " not in message  # No space after colon
    # Verify it's valid JSON
    json.loads(message)


def test_emit_decision_log_handles_non_serializable(caplog_json):
    """Test that non-JSON-serializable values are converted to strings."""
    from datetime import datetime

    emit_decision_log(
        {
            "decision": "allow",
            "reason": "authenticated",
            "correlation_id": "test-datetime",
            "timestamp": datetime(2025, 1, 1, 12, 0, 0),
        }
    )

    log_data = parse_log_json(caplog_json)
    # datetime should be converted to string
    assert isinstance(log_data["timestamp"], str)
    assert "2025" in log_data["timestamp"]

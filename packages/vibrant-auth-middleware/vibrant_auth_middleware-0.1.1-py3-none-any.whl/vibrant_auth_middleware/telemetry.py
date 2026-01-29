"""Structured logging helpers."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

LOGGER = logging.getLogger("vibrant_auth.telemetry")


def emit_decision_log(fields: Dict[str, Any]) -> None:
    """Emit a structured decision log as JSON."""

    payload = {"event": "auth_decision", **fields}
    try:
        LOGGER.info(json.dumps(payload, default=str, separators=(",", ":")))
    except Exception:  # pragma: no cover - logging failures should not break flow
        LOGGER.exception("failed to emit decision log", extra={"payload": payload})

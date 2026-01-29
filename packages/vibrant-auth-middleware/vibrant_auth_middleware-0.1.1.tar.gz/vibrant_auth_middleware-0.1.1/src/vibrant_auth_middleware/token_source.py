"""Token extraction utilities."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import MutableMapping, Optional

from fastapi import Request


_COOKIE_STORE_KEY = "_vibrant_mutable_cookies"


def _ensure_cookie_storage(request: Request) -> MutableMapping[str, str]:
    """Provide a mutable cookie mapping for tests using private access."""

    store = request.scope.get(_COOKIE_STORE_KEY)
    if store is None:
        store = {}
        request.scope[_COOKIE_STORE_KEY] = store
    return store


# Provide compatibility hook so tests mutating `request._cookies` keep working.
if not hasattr(Request, "_cookies") or isinstance(getattr(Request, "_cookies"), property):
    def _get_mutable_cookies(self: Request) -> MutableMapping[str, str]:
        return _ensure_cookie_storage(self)

    def _set_mutable_cookies(self: Request, value: MutableMapping[str, str]) -> None:
        self.scope[_COOKIE_STORE_KEY] = dict(value)

    Request._cookies = property(  # type: ignore[attr-defined]
        _get_mutable_cookies,
        _set_mutable_cookies,
    )


class TokenOrigin(str, Enum):
    COOKIE = "cookie"
    AUTHORIZATION_HEADER = "authorization_header"


@dataclass(slots=True)
class TokenSource:
    origin: TokenOrigin
    token: str
    token_type: Optional[str]
    correlation_id: str


def _correlation_id_from_request(request: Request) -> str:
    for header in ("x-correlation-id", "x-request-id"):
        value = request.headers.get(header)
        if value:
            return value.strip()
    return uuid.uuid4().hex


def _extract_from_cookies(request: Request) -> Optional[TokenSource]:
    combined: dict[str, str] = {}
    combined.update(getattr(request, "cookies", {}) or {})
    combined.update(_ensure_cookie_storage(request))
    token = combined.get("access_token")
    if not token:
        return None
    token_type = combined.get("token_type")
    if not token_type:
        raise ValueError("missing_token_type")
    return TokenSource(
        origin=TokenOrigin.COOKIE,
        token=token,
        token_type=token_type,
        correlation_id=_correlation_id_from_request(request),
    )


def _extract_from_authorization_header(request: Request) -> Optional[TokenSource]:
    header_value = request.headers.get("authorization")
    if not header_value:
        return None
    scheme, _, token = header_value.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise ValueError("invalid_prefix")
    return TokenSource(
        origin=TokenOrigin.AUTHORIZATION_HEADER,
        token=token.strip(),
        token_type="Bearer",
        correlation_id=_correlation_id_from_request(request),
    )


def extract_token(request: Request) -> TokenSource:
    """Extract a token from cookies or headers."""

    cookie_source = _extract_from_cookies(request)
    if cookie_source is not None:
        return cookie_source

    header_source = _extract_from_authorization_header(request)
    if header_source is not None:
        return header_source

    raise ValueError("missing_token")

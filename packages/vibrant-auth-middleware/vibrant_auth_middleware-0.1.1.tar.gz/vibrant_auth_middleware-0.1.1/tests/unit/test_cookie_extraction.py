import pytest
from fastapi import Request

from vibrant_auth_middleware.token_source import TokenOrigin, TokenSource, extract_token


def build_request(headers=None, cookies=None) -> Request:
    scope = {
        "type": "http",
        "headers": [],
        "method": "GET",
        "path": "/",
    }
    headers = headers or {}
    cookies = cookies or {}
    for key, value in headers.items():
        scope["headers"].append((key.lower().encode(), value.encode()))
    request = Request(scope)
    for name, value in cookies.items():
        request._cookies[name] = value  # type: ignore[attr-defined]
    return request


def test_extracts_token_from_cookies() -> None:
    request = build_request(cookies={"access_token": "jwt-cookie", "token_type": "Bearer"})
    source = extract_token(request)
    assert isinstance(source, TokenSource)
    assert source.origin == TokenOrigin.COOKIE
    assert source.token == "jwt-cookie"
    assert source.token_type == "JWT"


def test_missing_token_type_raises() -> None:
    request = build_request(cookies={"access_token": "jwt-cookie"})
    with pytest.raises(ValueError):
        extract_token(request)

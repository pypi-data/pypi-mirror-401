import pytest
from fastapi import Request

from vibrant_auth_middleware.token_source import TokenOrigin, TokenSource, extract_token


def build_request(headers=None) -> Request:
    scope = {
        "type": "http",
        "headers": [],
        "method": "GET",
        "path": "/",
    }
    headers = headers or {}
    for key, value in headers.items():
        scope["headers"].append((key.lower().encode(), value.encode()))
    return Request(scope)


def test_extracts_token_from_authorization_header() -> None:
    request = build_request(headers={"Authorization": "Bearer header.jwt"})
    source = extract_token(request)
    assert isinstance(source, TokenSource)
    assert source.origin == TokenOrigin.AUTHORIZATION_HEADER
    assert source.token == "header.jwt"
    assert source.token_type == "Bearer"


def test_invalid_header_prefix_raises() -> None:
    request = build_request(headers={"Authorization": "Token header.jwt"})
    with pytest.raises(ValueError):
        extract_token(request)

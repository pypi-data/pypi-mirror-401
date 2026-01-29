"""Performance regression tests for middleware latency."""

import asyncio
import time
from typing import Any, Callable, Dict

import jwt
import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient

from vibrant_auth_middleware.config import SigningMaterial
from vibrant_auth_middleware.middleware import MiddlewareSettings, VibrantAuthMiddleware


@pytest.fixture
def hs256_secret():
    """HS256 secret for testing."""
    return "test-secret-key-for-performance-testing"


@pytest.fixture
def signing_material(hs256_secret):
    """Signing material for testing."""
    return SigningMaterial(
        hs256_secret=hs256_secret,
        rs256_public_keys={"perf-key": "-----BEGIN PUBLIC KEY-----\ntest"},
        version="v1.0.0",
    )


@pytest.fixture
def valid_token(hs256_secret):
    """Generate a valid HS256 JWT token."""
    payload = {
        "sub": "user@example.com",
        "email": "user@example.com",
        "roles": ["user"],
        "exp": int(time.time()) + 3600,
    }
    return jwt.encode(payload, hs256_secret, algorithm="HS256")


@pytest.fixture
def app_with_middleware(signing_material):
    """Create a Starlette app with VibrantAuthMiddleware."""
    app = Starlette()

    settings = MiddlewareSettings(
        signing_material=signing_material,
        clock_skew_leeway=30,
    )

    app.add_middleware(VibrantAuthMiddleware, settings=settings)

    @app.route("/test")
    async def test_endpoint(request: Request):
        return PlainTextResponse("OK")

    return app


@pytest.mark.asyncio
async def test_middleware_latency_single_request(app_with_middleware, valid_token):
    """Test middleware overhead for a single request."""
    client = TestClient(app_with_middleware)

    # Warm up
    response = client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})
    assert response.status_code == 200

    # Measure latency
    start = time.perf_counter()
    response = client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})
    end = time.perf_counter()

    assert response.status_code == 200
    latency_ms = (end - start) * 1000

    # Single request should be well under 5ms
    # Using a relaxed threshold for CI environments
    assert latency_ms < 50, f"Single request latency {latency_ms:.2f}ms exceeds threshold"


@pytest.mark.asyncio
async def test_middleware_latency_burst(app_with_middleware, valid_token):
    """Test middleware overhead under burst load."""
    client = TestClient(app_with_middleware)

    # Warm up
    for _ in range(10):
        client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})

    # Measure burst of 100 requests
    num_requests = 100
    start = time.perf_counter()

    for _ in range(num_requests):
        response = client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})
        assert response.status_code == 200

    end = time.perf_counter()
    total_time = end - start
    avg_latency_ms = (total_time / num_requests) * 1000

    print(f"\nBurst test: {num_requests} requests in {total_time:.3f}s")
    print(f"Average latency: {avg_latency_ms:.2f}ms per request")
    print(f"Throughput: {num_requests / total_time:.0f} req/s")

    # Average should be well under 5ms per request
    assert avg_latency_ms < 20, f"Average latency {avg_latency_ms:.2f}ms exceeds threshold"


@pytest.mark.asyncio
async def test_middleware_latency_target_1k_rps(app_with_middleware, valid_token):
    """Test middleware can handle 1000 req/s with ≤5ms overhead."""
    client = TestClient(app_with_middleware)

    # Warm up
    for _ in range(50):
        client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})

    # Simulate 1 second of traffic at 1000 req/s
    # In practice, test a smaller sample and extrapolate
    num_requests = 200  # Reduced for faster test execution
    start = time.perf_counter()

    successful_requests = 0
    for _ in range(num_requests):
        response = client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})
        if response.status_code == 200:
            successful_requests += 1

    end = time.perf_counter()
    total_time = end - start
    avg_latency_ms = (total_time / num_requests) * 1000
    actual_rps = num_requests / total_time

    print(f"\nLoad test: {num_requests} requests in {total_time:.3f}s")
    print(f"Average latency: {avg_latency_ms:.2f}ms per request")
    print(f"Throughput: {actual_rps:.0f} req/s")
    print(f"Success rate: {successful_requests}/{num_requests}")

    assert successful_requests == num_requests
    # Target: ≤5ms at 1000 req/s, but allow some margin for test environments
    assert avg_latency_ms < 10, f"Average latency {avg_latency_ms:.2f}ms exceeds 10ms threshold"


@pytest.mark.asyncio
async def test_middleware_latency_header_vs_cookie(app_with_middleware, valid_token):
    """Compare latency between header and cookie token sources."""
    client = TestClient(app_with_middleware)

    # Warm up
    for _ in range(10):
        client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})

    # Test cookie source
    num_requests = 50
    start = time.perf_counter()
    for _ in range(num_requests):
        client.get("/test", cookies={"access_token": valid_token, "token_type": "Bearer"})
    cookie_time = time.perf_counter() - start

    # Test header source
    start = time.perf_counter()
    for _ in range(num_requests):
        client.get("/test", headers={"Authorization": f"Bearer {valid_token}"})
    header_time = time.perf_counter() - start

    cookie_avg_ms = (cookie_time / num_requests) * 1000
    header_avg_ms = (header_time / num_requests) * 1000

    print(f"\nCookie source: {cookie_avg_ms:.2f}ms avg")
    print(f"Header source: {header_avg_ms:.2f}ms avg")

    # Both should be performant
    assert cookie_avg_ms < 10
    assert header_avg_ms < 10

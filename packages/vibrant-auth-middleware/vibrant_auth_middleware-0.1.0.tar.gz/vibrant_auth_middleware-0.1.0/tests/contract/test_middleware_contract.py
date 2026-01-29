"""Contract tests for middleware initialization."""

import pytest
from fastapi import FastAPI

from vibrant_auth_middleware import (
    VibrantAuthMiddleware,
    MiddlewareSettings,
    SigningMaterial,
)


# ===== Valid Initialization Tests (T002-T004) =====


def test_valid_initialization_with_minimal_material():
    """
    T002: Valid SigningMaterial initialization.
    Reference: contracts/initialization-contract.md Scenario 1
    """
    app = FastAPI()

    material = SigningMaterial(
        hs256_secret="test-secret-key-min-32-characters-long",
        rs256_public_keys={"default": "-----BEGIN PUBLIC KEY-----\nMIIBIj..."},
        version="1.0.0"
    )
    settings = MiddlewareSettings(signing_material=material)
    middleware = VibrantAuthMiddleware(app, settings)

    # Middleware should be initialized with material immediately available
    assert middleware._material == material
    assert middleware._material.version == "1.0.0"


def test_valid_initialization_with_multiple_rs256_keys():
    """
    T003: Material with multiple RS256 keys in dict succeeds.
    Reference: contracts/initialization-contract.md Scenario 2
    """
    app = FastAPI()

    material = SigningMaterial(
        hs256_secret="test-secret",
        rs256_public_keys={
            "key-2024-01": "-----BEGIN PUBLIC KEY-----\n...",
            "key-2024-02": "-----BEGIN PUBLIC KEY-----\n...",
            "key-2024-03": "-----BEGIN PUBLIC KEY-----\n..."
        },
        version="2024.1"
    )
    settings = MiddlewareSettings(signing_material=material)
    middleware = VibrantAuthMiddleware(app, settings)

    assert middleware._material == material
    assert len(middleware._material.rs256_public_keys) == 3


def test_valid_initialization_with_custom_clock_skew():
    """
    T004: MiddlewareSettings with custom clock_skew_leeway succeeds.
    Reference: contracts/initialization-contract.md Scenario 3
    """
    app = FastAPI()

    material = SigningMaterial(
        hs256_secret="test-secret",
        rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
        version="1.0"
    )
    settings = MiddlewareSettings(
        signing_material=material,
        clock_skew_leeway=10  # Custom value
    )
    middleware = VibrantAuthMiddleware(app, settings)

    assert middleware.settings.clock_skew_leeway == 10


# ===== Validation Error Tests (T005-T009) =====


def test_missing_hs256_secret():
    """
    T005: SigningMaterial with empty hs256_secret raises ValueError.
    Reference: contracts/initialization-contract.md Error 2
    """
    app = FastAPI()

    with pytest.raises(ValueError, match="Signing material must include hs256_secret"):
        material = SigningMaterial(
            hs256_secret="",  # Empty
            rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
            version="1.0"
        )
        settings = MiddlewareSettings(signing_material=material)
        VibrantAuthMiddleware(app, settings)


def test_empty_rs256_public_keys():
    """
    T006: SigningMaterial with {} rs256_public_keys raises ValueError.
    Reference: contracts/initialization-contract.md Error 3
    """
    app = FastAPI()

    with pytest.raises(ValueError, match="Signing material must include at least one RS256 public key"):
        material = SigningMaterial(
            hs256_secret="test-secret",
            rs256_public_keys={},  # Empty dict
            version="1.0"
        )
        settings = MiddlewareSettings(signing_material=material)
        VibrantAuthMiddleware(app, settings)


def test_missing_version():
    """
    T007: SigningMaterial with empty version raises ValueError.
    Reference: contracts/initialization-contract.md Error 4
    """
    app = FastAPI()

    with pytest.raises(ValueError, match="Signing material must include version identifier"):
        material = SigningMaterial(
            hs256_secret="test-secret",
            rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
            version=""  # Empty
        )
        settings = MiddlewareSettings(signing_material=material)
        VibrantAuthMiddleware(app, settings)


def test_invalid_rs256_key_value():
    """
    T008: SigningMaterial with empty RS256 key value raises ValueError.
    Reference: contracts/initialization-contract.md Error 5
    """
    app = FastAPI()

    with pytest.raises(ValueError, match=r"RS256 public key for kid 'key-2' must be non-empty"):
        material = SigningMaterial(
            hs256_secret="test-secret",
            rs256_public_keys={"key-1": "-----BEGIN PUBLIC KEY-----\n...", "key-2": ""},
            version="1.0"
        )
        settings = MiddlewareSettings(signing_material=material)
        VibrantAuthMiddleware(app, settings)


def test_wrong_settings_type():
    """
    T009: VibrantAuthMiddleware with dict instead of MiddlewareSettings raises TypeError.
    Reference: contracts/initialization-contract.md Error 6
    """
    app = FastAPI()

    material = SigningMaterial(
        hs256_secret="test-secret",
        rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
        version="1.0"
    )

    with pytest.raises(TypeError, match="settings must be MiddlewareSettings instance"):
        # Passing a dict instead of MiddlewareSettings
        VibrantAuthMiddleware(app, {"signing_material": material})

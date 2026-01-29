"""Signing material management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True, frozen=True)
class SigningMaterial:
    """
    Cryptographic material for JWT verification.

    All fields are required. Material is immutable after construction.
    To update signing material, restart the middleware with new material.
    """
    hs256_secret: str  # Required: HMAC secret for HS256 tokens
    rs256_public_keys: Dict[str, str]  # Required: kid → PEM public key mapping
    version: str  # Required: Version identifier for tracking/debugging


def _validate_signing_material(material: SigningMaterial) -> None:
    """
    Validate signing material structure and content.

    Raises:
        ValueError: If material is invalid with specific error message
    """
    if not material:
        raise ValueError("Signing material is required")

    if not material.hs256_secret:
        raise ValueError("Signing material must include hs256_secret")

    if not isinstance(material.rs256_public_keys, dict):
        raise ValueError("rs256_public_keys must be a dictionary")

    if not material.rs256_public_keys:
        raise ValueError("Signing material must include at least one RS256 public key")

    for kid, pem_key in material.rs256_public_keys.items():
        if not pem_key:
            raise ValueError(f"RS256 public key for kid '{kid}' must be non-empty")

    if not material.version:
        raise ValueError("Signing material must include version identifier")

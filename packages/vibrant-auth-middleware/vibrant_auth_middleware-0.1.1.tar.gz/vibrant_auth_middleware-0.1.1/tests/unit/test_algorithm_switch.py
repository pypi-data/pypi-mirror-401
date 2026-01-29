import pytest
import jwt

from vibrant_auth_middleware.config import SigningMaterial
from vibrant_auth_middleware.decisions import verify_token

HS_SECRET = "super-secret"

RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBALYJv1nV0qB5qL9xLpm2bhs6V14XmA0I+XtLWPSDcAp+aFByZTn8
f1vGDdEPxt9ZhUceqdiEWZJ1V8zZIvNl918CAwEAAQJAYAvyv4h+OKX3FfCgAS/p
7YQxORP9ix9C0H0v9d0d7aTcsFR9S8Ku3ZjW0ccmiXVxZd0odzA/XFqOeE2fcOgx
lQIhAPY8GllHvI6j1N4yY8kHMCmBbirPiD7dAk5doEKBaFt7AiEAu8CFu+nwfr3Q
2TKiYd+/jCLqshFVv+/mv0QVlz3LSJ8CIHZQG3Y0TLzl5FK+KFLATeWk0dBs7FBX
2jciYGiNIPixAiEAqs4ITPHZhHtBeAaPugZq5j7BFbS+WFxiXj6827U/5UkCIHhL
AH2aopG9InCRTgGrDWJA3eXvYaNhR2RbUiXecrKF
-----END RSA PRIVATE KEY-----"""

RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALYJv1nV0qB5qL9xLpm2bhs6V14XmA0I
+XtLWPSDcAp+aFByZTn8f1vGDdEPxt9ZhUceqdiEWZJ1V8zZIvNl918CAwEAAQ==
-----END PUBLIC KEY-----"""


@pytest.fixture
def signing_material() -> SigningMaterial:
    return SigningMaterial(
        hs256_secret=HS_SECRET,
        rs256_public_keys={"kid-1": RSA_PUBLIC_KEY},
        version="1",
    )


def encode_hs(payload):
    return jwt.encode(payload, HS_SECRET, algorithm="HS256")


def encode_rs(payload):
    return jwt.encode(payload, RSA_PRIVATE_KEY, algorithm="RS256", headers={"kid": "kid-1"})


def test_verifies_hs256(signing_material):
    token = encode_hs({"sub": "user-123"})
    claims = verify_token(token, signing_material)
    assert claims["sub"] == "user-123"


def test_verifies_rs256(signing_material):
    token = encode_rs({"sub": "user-456"})
    claims = verify_token(token, signing_material)
    assert claims["sub"] == "user-456"


def test_unsupported_algorithm(signing_material):
    token = jwt.encode({"sub": "user"}, HS_SECRET, algorithm="HS512")
    with pytest.raises(ValueError):
        verify_token(token, signing_material)

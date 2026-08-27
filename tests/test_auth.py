"""Unit tests for Cognito JWT verification.

Strategy:
- Generate a real RSA key pair in-process (no AWS calls).
- Build JWT tokens with the correct claims, sign them with the private key.
- Mock PyJWKClient so verify_token fetches the matching public key.
- Test happy path, expiry, wrong audience, wrong issuer, missing sub, and
  group extraction.

Run with:
    pytest tests/test_auth.py -v
"""

import time
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt as pyjwt

from backend.auth.cognito import verify_token
from backend.auth.models import StudentUser

# ── Fixtures ──────────────────────────────────────────────────────────────────

FAKE_REGION = "eu-west-2"
FAKE_POOL_ID = "eu-west-2_TestPoolXX"
FAKE_CLIENT_ID = "test-client-id-abc123"
FAKE_ISSUER = f"https://cognito-idp.{FAKE_REGION}.amazonaws.com/{FAKE_POOL_ID}"


@pytest.fixture(scope="module")
def rsa_key_pair():
    """Generate a one-time RSA key pair for signing test JWTs."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture(scope="module")
def mock_signing_key(rsa_key_pair):
    """Return a mock PyJWKS signing key wrapping the test RSA public key."""
    _, public_key = rsa_key_pair
    mock_key = MagicMock()
    mock_key.key = public_key
    return mock_key


def build_token(
    private_key,
    *,
    sub: str = "user-sub-12345",
    email: str = "student@example.com",
    client_id: str = FAKE_CLIENT_ID,
    issuer: str = FAKE_ISSUER,
    exp_offset: int = 3600,
    groups: list[str] | None = None,
    cohort: str | None = "aug-2026",
    enrollment_date: str | None = "2026-08-01",
    given_name: str | None = "Alice",
    family_name: str | None = "Smith",
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Build and sign a JWT with the given claims."""
    now = int(time.time())
    payload: dict[str, Any] = {
        "sub": sub,
        "email": email,
        "aud": client_id,
        "iss": issuer,
        "iat": now,
        "exp": now + exp_offset,
        "token_use": "access",
    }
    if groups is not None:
        payload["cognito:groups"] = groups
    if cohort:
        payload["custom:cohort"] = cohort
    if enrollment_date:
        payload["custom:enrollment_date"] = enrollment_date
    if given_name:
        payload["given_name"] = given_name
    if family_name:
        payload["family_name"] = family_name
    if extra_claims:
        payload.update(extra_claims)

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pyjwt.encode(payload, private_pem, algorithm="RS256")


# ── Helpers ───────────────────────────────────────────────────────────────────

def patch_env_and_jwks(mock_signing_key):
    """Return a context manager that patches env vars and the JWKS client."""
    env_patch = patch.dict(
        "os.environ",
        {
            "COGNITO_REGION": FAKE_REGION,
            "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
            "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
        },
    )
    jwks_patch = patch("backend.auth.cognito._get_jwks_client")
    return env_patch, jwks_patch


# ── Tests ─────────────────────────────────────────────────────────────────────


class TestVerifyTokenHappyPath:
    """verify_token returns a correct StudentUser for a valid JWT."""

    def test_returns_student_user(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key)

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            # Re-import to pick up patched env
            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            user = cognito_module.verify_token(token)

        assert isinstance(user, StudentUser)
        assert user.id == "user-sub-12345"
        assert user.email == "student@example.com"
        assert user.cohort == "aug-2026"
        assert user.enrollment_date == "2026-08-01"
        assert user.given_name == "Alice"
        assert user.family_name == "Smith"

    def test_extracts_groups(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key, groups=["instructors", "students"])

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            user = cognito_module.verify_token(token)

        assert "instructors" in user.groups
        assert user.is_instructor is True

    def test_student_group_not_instructor(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key, groups=["students"])

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            user = cognito_module.verify_token(token)

        assert user.is_instructor is False

    def test_no_groups_defaults_to_empty_list(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key, groups=None)

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            user = cognito_module.verify_token(token)

        assert user.groups == []

    def test_optional_custom_attributes_default_to_none(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key, cohort=None, enrollment_date=None)

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            user = cognito_module.verify_token(token)

        assert user.cohort is None
        assert user.enrollment_date is None


class TestVerifyTokenFailures:
    """verify_token raises InvalidTokenError for invalid tokens."""

    def test_expired_token_raises(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        # Token expired 60 seconds ago
        token = build_token(private_key, exp_offset=-60)

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            with pytest.raises(pyjwt.ExpiredSignatureError):
                cognito_module.verify_token(token)

    def test_wrong_audience_raises(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key, client_id="wrong-client-id")

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            with pytest.raises(pyjwt.InvalidAudienceError):
                cognito_module.verify_token(token)

    def test_wrong_issuer_raises(self, rsa_key_pair, mock_signing_key):
        private_key, _ = rsa_key_pair
        token = build_token(private_key, issuer="https://evil.example.com/pool")

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            with pytest.raises(pyjwt.InvalidIssuerError):
                cognito_module.verify_token(token)

    def test_tampered_token_raises(self, rsa_key_pair, mock_signing_key):
        """Modifying the token payload should break the RS256 signature."""
        private_key, _ = rsa_key_pair
        token = build_token(private_key)

        # Flip a byte in the signature part
        header, payload, sig = token.split(".")
        tampered = f"{header}.{payload}.{sig[:-4]}XXXX"

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.return_value = mock_signing_key
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            with pytest.raises(pyjwt.InvalidTokenError):
                cognito_module.verify_token(tampered)

    def test_jwks_key_lookup_failure_raises(self, rsa_key_pair):
        """JWKS lookup failures are wrapped as InvalidTokenError."""
        from jwt import PyJWKClientError

        private_key, _ = rsa_key_pair
        token = build_token(private_key)

        with (
            patch.dict(
                "os.environ",
                {
                    "COGNITO_REGION": FAKE_REGION,
                    "COGNITO_USER_POOL_ID": FAKE_POOL_ID,
                    "COGNITO_APP_CLIENT_ID": FAKE_CLIENT_ID,
                },
            ),
            patch("backend.auth.cognito._get_jwks_client") as mock_client_fn,
        ):
            mock_client = MagicMock()
            mock_client.get_signing_key_from_jwt.side_effect = PyJWKClientError("no key found")
            mock_client_fn.return_value = mock_client

            import importlib
            import backend.auth.cognito as cognito_module
            importlib.reload(cognito_module)

            with pytest.raises(pyjwt.InvalidTokenError):
                cognito_module.verify_token(token)


# ── StudentUser model tests ───────────────────────────────────────────────────


class TestStudentUserModel:
    """Unit tests for the StudentUser Pydantic model."""

    def test_display_name_full_name(self):
        user = StudentUser(id="abc", email="a@b.com", given_name="Bob", family_name="Jones")
        assert user.display_name == "Bob Jones"

    def test_display_name_falls_back_to_email_prefix(self):
        user = StudentUser(id="abc", email="johndoe@example.com")
        assert user.display_name == "johndoe"

    def test_is_instructor_true(self):
        user = StudentUser(id="abc", email="a@b.com", groups=["instructors"])
        assert user.is_instructor is True

    def test_is_instructor_false_for_student(self):
        user = StudentUser(id="abc", email="a@b.com", groups=["students"])
        assert user.is_instructor is False

    def test_empty_id_raises_validation_error(self):
        with pytest.raises(Exception):  # pydantic ValidationError
            StudentUser(id="   ", email="a@b.com")

    def test_groups_defaults_to_empty_list(self):
        user = StudentUser(id="abc", email="a@b.com")
        assert user.groups == []

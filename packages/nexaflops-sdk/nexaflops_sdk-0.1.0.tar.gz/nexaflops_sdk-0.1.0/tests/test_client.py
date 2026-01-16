"""Tests for NexaflopsClient."""

import pytest
from unittest.mock import patch

from nexaflops_sdk import NexaflopsClient
from nexaflops_sdk.exceptions import AuthenticationError


class TestClientInitialization:
    """Tests for client initialization and configuration."""

    def test_valid_api_key_live(self) -> None:
        """Test client accepts valid live API key."""
        client = NexaflopsClient(api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345")
        assert client is not None
        client.close()

    def test_valid_api_key_test(self) -> None:
        """Test client accepts valid test API key."""
        client = NexaflopsClient(api_key="nxf_test_abcdefghijklmnopqrstuvwxyz012345")
        assert client is not None
        client.close()

    def test_invalid_api_key_empty(self) -> None:
        """Test client rejects empty API key."""
        with pytest.raises(AuthenticationError) as exc_info:
            NexaflopsClient(api_key="")
        assert "API key is required" in str(exc_info.value)

    def test_invalid_api_key_format(self) -> None:
        """Test client rejects invalid API key format."""
        with pytest.raises(AuthenticationError) as exc_info:
            NexaflopsClient(api_key="invalid_key_format")
        assert "Invalid API key format" in str(exc_info.value)

    def test_invalid_api_key_too_short(self) -> None:
        """Test client rejects too-short API key."""
        with pytest.raises(AuthenticationError) as exc_info:
            NexaflopsClient(api_key="nxf_live_short")
        assert "too short" in str(exc_info.value)

    def test_custom_base_url(self) -> None:
        """Test client accepts custom base URL."""
        client = NexaflopsClient(
            api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345",
            base_url="https://custom.api.example.com",
        )
        assert client._base_url == "https://custom.api.example.com"
        client.close()

    def test_base_url_trailing_slash_stripped(self) -> None:
        """Test trailing slash is stripped from base URL."""
        client = NexaflopsClient(
            api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345",
            base_url="https://api.example.com/",
        )
        assert client._base_url == "https://api.example.com"
        client.close()

    def test_context_manager(self) -> None:
        """Test client works as context manager."""
        with NexaflopsClient(
            api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345"
        ) as client:
            assert client is not None
            assert hasattr(client, "licenses")


class TestFingerprint:
    """Tests for fingerprint generation."""

    def test_get_fingerprint_returns_sha256(self) -> None:
        """Test fingerprint is valid SHA-256 hex string."""
        with NexaflopsClient(
            api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345"
        ) as client:
            fp = client.get_fingerprint()
            assert len(fp) == 64  # SHA-256 hex is 64 chars
            assert all(c in "0123456789abcdef" for c in fp)

    def test_fingerprint_deterministic(self) -> None:
        """Test fingerprint is deterministic for same host."""
        with NexaflopsClient(
            api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345"
        ) as client:
            fp1 = client.get_fingerprint()
            fp2 = client.get_fingerprint()
            assert fp1 == fp2

    def test_get_fingerprint_info(self) -> None:
        """Test fingerprint info returns expected keys."""
        with NexaflopsClient(
            api_key="nxf_live_abcdefghijklmnopqrstuvwxyz012345"
        ) as client:
            info = client.get_fingerprint_info()
            assert "cpu" in info
            assert "mac" in info
            assert "hostname" in info
            assert "fingerprint" in info

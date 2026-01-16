"""
Integration tests for NEXAFLOPS Python SDK against Control Plane API.

These tests require a running Control Plane server at http://localhost:8080.
Run with: pytest tests/integration/ -v

Prerequisites:
    cd control-plane && mvn spring-boot:run
"""

import os
import pytest
import httpx

from nexaflops_sdk import NexaflopsClient
from nexaflops_sdk.exceptions import AuthenticationError


CONTROL_PLANE_URL = os.getenv("NEXAFLOPS_API_URL", "http://localhost:8080")
TEST_API_KEY = os.getenv(
    "NEXAFLOPS_API_KEY", "nxf_test_abcdefghijklmnopqrstuvwxyz012345"
)


def is_server_running() -> bool:
    """Check if Control Plane server is running."""
    try:
        response = httpx.get(f"{CONTROL_PLANE_URL}/actuator/health", timeout=5.0)
        return response.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not is_server_running(), reason="Control Plane server not running at localhost:8080"
)


class TestLicenseIntegration:
    """Integration tests for license operations."""

    @pytest.fixture
    def client(self):
        """Create client configured for local Control Plane."""
        return NexaflopsClient(
            api_key=TEST_API_KEY,
            base_url=CONTROL_PLANE_URL,
        )

    def _issue_license(self, tier: str = "PROFESSIONAL") -> str:
        """Issue a test license via HTTP and return its ID."""
        response = httpx.post(
            f"{CONTROL_PLANE_URL}/api/v1/licenses",
            headers={
                "X-API-Key": TEST_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "customerId": "pytest-integration",
                "organization": "Pytest Integration Test",
                "tier": tier,
                "durationDays": 30,
            },
            timeout=10.0,
        )
        assert response.status_code == 201
        return response.json()["id"]

    def test_validate_license_success(self, client):
        """Test successful license validation."""
        license_id = self._issue_license()
        fingerprint = client.get_fingerprint()

        result = client.licenses.validate(
            license_id=license_id,
            host_fingerprint=fingerprint,
        )

        assert result.valid is True
        assert result.license_id == license_id

    def test_validate_license_not_found(self, client):
        """Test validation of non-existent license returns invalid result."""
        from nexaflops_sdk.exceptions import LicenseValidationError

        fake_id = "00000000-0000-0000-0000-000000000000"
        fingerprint = client.get_fingerprint()

        # SDK returns 403 which raises exception
        with pytest.raises(LicenseValidationError):
            client.licenses.validate(
                license_id=fake_id,
                host_fingerprint=fingerprint,
            )

    def test_get_license_success(self, client):
        """Test retrieving license details."""
        license_id = self._issue_license()

        license_obj = client.licenses.get(license_id)

        assert license_obj.id == license_id
        assert "compiler" in license_obj.features

    def test_fingerprint_generation(self, client):
        """Test fingerprint generation is deterministic."""
        fp1 = client.get_fingerprint()
        fp2 = client.get_fingerprint()

        assert fp1 == fp2
        assert len(fp1) == 64
        assert all(c in "0123456789abcdef" for c in fp1)

    def test_client_with_invalid_key(self):
        """Test client rejects invalid API key format."""
        with pytest.raises(AuthenticationError):
            NexaflopsClient(api_key="invalid_key")

    def test_full_license_lifecycle(self, client):
        """Test issue -> validate -> get flow."""
        license_id = self._issue_license("ENTERPRISE")
        fingerprint = client.get_fingerprint()

        result = client.licenses.validate(license_id, fingerprint)
        assert result.valid is True

        license_obj = client.licenses.get(license_id)
        assert license_obj.id == license_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

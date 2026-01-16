"""
License operations for NEXAFLOPS SDK.

This module provides the LicenseClient class which handles all license-related
API operations including validation, retrieval, and management.
"""

from typing import Optional

import httpx

from nexaflops_sdk.exceptions import (
    AuthenticationError,
    HostMismatchError,
    LicenseExpiredError,
    LicenseRevokedError,
    LicenseValidationError,
    NetworkError,
    NexaflopsError,
    RateLimitError,
)
from nexaflops_sdk.models import (
    License,
    LicenseIssueRequest,
    ValidationResult,
)


class LicenseClient:
    """Client for license-related API operations.

    This class is not meant to be instantiated directly. Use the
    `licenses` property of NexaflopsClient instead.
    """

    def __init__(self, http_client: httpx.Client, base_url: str) -> None:
        """Initialize license client.

        Args:
            http_client: Configured httpx client with auth headers
            base_url: Base URL of the Control Plane API
        """
        self._client = http_client
        self._base_url = base_url.rstrip("/")

    def validate(
        self,
        license_id: str,
        host_fingerprint: str,
        raise_on_invalid: bool = False,
    ) -> ValidationResult:
        """Validate a license for the current host.

        This is the primary method for runtime license validation in ML
        training pipelines. It verifies that the license is active, not
        expired, and bound to the correct host.

        Args:
            license_id: UUID of the license to validate
            host_fingerprint: SHA-256 fingerprint of the current host
            raise_on_invalid: If True, raise exception on validation failure

        Returns:
            ValidationResult with validation status and details

        Raises:
            LicenseValidationError: If raise_on_invalid is True and validation fails
            AuthenticationError: If API key is invalid
            NetworkError: If network request fails
        """
        url = f"{self._base_url}/api/v1/licenses/validate"
        payload = {
            "licenseId": license_id,
            "hostFingerprint": host_fingerprint,
        }

        try:
            response = self._client.post(url, json=payload)
        except httpx.RequestError as e:
            raise NetworkError(f"Request failed: {e}", cause=e) from e

        self._handle_error_response(response)

        try:
            data = response.json()
        except ValueError as e:
            raise NetworkError("Invalid JSON response from server", cause=e) from e

        result = ValidationResult(
            valid=data.get("valid", False),
            license_id=license_id,
            tier=data.get("tier"),
            expires_at=data.get("expiresAt"),
            reason=data.get("reason"),
            features=data.get("features", {}),
        )

        if raise_on_invalid and not result.valid:
            self._raise_validation_exception(result)

        return result

    def get(self, license_id: str) -> License:
        """Get license details by ID.

        Args:
            license_id: UUID of the license

        Returns:
            License object with full details

        Raises:
            NexaflopsError: If license not found or request fails
        """
        url = f"{self._base_url}/api/v1/licenses/{license_id}"

        try:
            response = self._client.get(url)
        except httpx.RequestError as e:
            raise NetworkError(f"Request failed: {e}", cause=e) from e

        self._handle_error_response(response)

        data = response.json()
        return License(
            id=data["id"],
            organization_name=data.get(
                "organization", data.get("organizationName", "")
            ),
            tier=data["tier"],
            status=data["status"],
            issued_at=data["issuedAt"],
            expires_at=data["expiresAt"],
            max_hosts=data.get("maxHosts", 1),
            features=data.get("features", {}),
            limits=data.get("limits", {}),
        )

    def issue(self, request: LicenseIssueRequest) -> License:
        """Issue a new license (admin operation).

        Note: This operation requires admin-level API key permissions.

        Args:
            request: License issue request with organization and tier info

        Returns:
            Newly issued License object

        Raises:
            AuthenticationError: If API key lacks admin permissions
        """
        url = f"{self._base_url}/api/v1/licenses"

        try:
            response = self._client.post(url, json=request.model_dump())
        except httpx.RequestError as e:
            raise NetworkError(f"Request failed: {e}", cause=e) from e

        self._handle_error_response(response)

        data = response.json()
        return License(
            id=data["id"],
            organization_name=data["organizationName"],
            tier=data["tier"],
            status=data["status"],
            issued_at=data["issuedAt"],
            expires_at=data["expiresAt"],
            max_hosts=data.get("maxHosts", 1),
            features=data.get("features", {}),
            limits=data.get("limits", {}),
        )

    def revoke(self, license_id: str, reason: Optional[str] = None) -> bool:
        """Revoke a license (admin operation).

        Once revoked, a license cannot be reinstated.

        Args:
            license_id: UUID of the license to revoke
            reason: Optional reason for revocation

        Returns:
            True if revocation succeeded

        Raises:
            AuthenticationError: If API key lacks admin permissions
        """
        url = f"{self._base_url}/api/v1/licenses/{license_id}"

        try:
            response = self._client.delete(
                url, params={"reason": reason} if reason else None
            )
        except httpx.RequestError as e:
            raise NetworkError(f"Request failed: {e}", cause=e) from e

        self._handle_error_response(response)
        return response.status_code == 204

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Handle HTTP error responses."""
        if response.status_code == 200 or response.status_code == 204:
            return

        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API key")

        if response.status_code == 403:
            try:
                data = response.json()
                raise LicenseValidationError(
                    message=data.get("message", "Access denied"),
                    reason=data.get("reason"),
                )
            except ValueError:
                raise LicenseValidationError("Access denied") from None

        if response.status_code == 404:
            raise NexaflopsError("License not found", status_code=404)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None,
            )

        raise NexaflopsError(
            f"API request failed: {response.text}",
            status_code=response.status_code,
        )

    def _raise_validation_exception(self, result: ValidationResult) -> None:
        """Raise appropriate exception based on validation result."""
        reason = result.reason or "UNKNOWN"

        if reason == "EXPIRED":
            raise LicenseExpiredError(
                license_id=result.license_id,
                expired_at=str(result.expires_at),
            )

        if reason == "REVOKED":
            raise LicenseRevokedError(license_id=result.license_id)

        if reason == "HOST_MISMATCH":
            raise HostMismatchError(license_id=result.license_id)

        raise LicenseValidationError(
            message=f"License validation failed: {reason}",
            license_id=result.license_id,
            reason=reason,
        )

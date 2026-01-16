"""
Main client class for NEXAFLOPS SDK.

The NexaflopsClient is the primary entry point for interacting with the
NEXAFLOPS Control Plane API. It provides a unified interface for license
validation and management.

Usage:
    client = NexaflopsClient(api_key="nxf_live_xxx")
    result = client.licenses.validate("license-id", client.get_fingerprint())
"""

from typing import Optional

import httpx

from nexaflops_sdk._version import __version__
from nexaflops_sdk.exceptions import AuthenticationError
from nexaflops_sdk.fingerprint import compute_fingerprint, get_fingerprint_info
from nexaflops_sdk.licenses import LicenseClient

# Default API endpoint
DEFAULT_BASE_URL = "https://api.nexaflops.io"

# Default timeout configuration (seconds)
DEFAULT_TIMEOUT = httpx.Timeout(
    connect=5.0,  # Connection establishment timeout
    read=30.0,  # Response read timeout
    write=10.0,  # Request write timeout
    pool=5.0,  # Connection pool waiting timeout
)

# Retry configuration
DEFAULT_MAX_RETRIES = 3


class NexaflopsClient:
    """Client for the NEXAFLOPS Control Plane API.

    This is the main entry point for the SDK. It handles authentication,
    connection management, and provides access to resource-specific clients.

    Attributes:
        licenses: LicenseClient for license operations

    Example:
        client = NexaflopsClient(
            api_key="nxf_live_xxx",
            base_url="https://api.nexaflops.io"
        )

        # Validate license
        result = client.licenses.validate(
            license_id="uuid-here",
            host_fingerprint=client.get_fingerprint()
        )

        if result.valid:
            print(f"Valid until {result.expires_at}")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Optional[httpx.Timeout] = None,
        verify_ssl: bool = True,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        """Initialize the NEXAFLOPS client.

        Args:
            api_key: API key for authentication (format: nxf_live_xxx or nxf_test_xxx)
            base_url: Base URL of the Control Plane API
            timeout: Custom timeout configuration
            verify_ssl: Whether to verify SSL certificates (disable only for testing)
            max_retries: Maximum number of retry attempts for failed requests

        Raises:
            AuthenticationError: If API key format is invalid
        """
        self._validate_api_key(api_key)

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries

        # Configure HTTP client
        self._http_client = httpx.Client(
            headers=self._build_headers(),
            timeout=timeout or DEFAULT_TIMEOUT,
            verify=verify_ssl,
            follow_redirects=False,  # Security: do not follow redirects
        )

        # Initialize resource clients
        self._licenses = LicenseClient(self._http_client, self._base_url)

    @property
    def licenses(self) -> LicenseClient:
        """Get the license operations client."""
        return self._licenses

    def get_fingerprint(self, include_hostname: bool = False) -> str:
        """Get the current host fingerprint for license validation.

        The fingerprint is a SHA-256 hash of hardware identifiers (CPU, MAC).
        This value should be passed to license validation requests.

        Args:
            include_hostname: Include hostname in fingerprint (False for containers)

        Returns:
            SHA-256 hex digest string (64 characters)
        """
        return compute_fingerprint(include_hostname=include_hostname)

    def get_fingerprint_info(self) -> dict[str, Optional[str]]:
        """Get detailed fingerprint component information.

        This is useful for debugging fingerprint mismatches.
        Returns raw component values (not hashed).

        Returns:
            Dictionary with fingerprint components
        """
        return get_fingerprint_info()

    def close(self) -> None:
        """Close the HTTP client and release resources.

        This should be called when the client is no longer needed,
        or use the client as a context manager.
        """
        self._http_client.close()

    def __enter__(self) -> "NexaflopsClient":
        """Enter context manager."""
        return self

    def __exit__(self, *args: object) -> None:
        """Exit context manager and close client."""
        self.close()

    def _validate_api_key(self, api_key: str) -> None:
        """Validate API key format.

        Valid formats:
        - nxf_live_<32+ chars> (production)
        - nxf_test_<32+ chars> (testing)

        Raises:
            AuthenticationError: If format is invalid
        """
        if not api_key:
            raise AuthenticationError("API key is required")

        if not api_key.startswith(("nxf_live_", "nxf_test_")):
            raise AuthenticationError(
                "Invalid API key format. Expected 'nxf_live_...' or 'nxf_test_...'"
            )

        # Extract the actual key part
        key_part = api_key.split("_", 2)[-1]
        if len(key_part) < 32:
            raise AuthenticationError(
                "API key is too short. Ensure you're using the full key."
            )

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for API requests."""
        return {
            "X-API-Key": self._api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"nexaflops-sdk-python/{__version__}",
        }

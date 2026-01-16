"""
Custom exceptions for NEXAFLOPS SDK.

Exception Hierarchy:
    NexaflopsError (base)
    ├── AuthenticationError
    ├── LicenseValidationError
    ├── RateLimitError
    └── NetworkError
"""

from typing import Optional


class NexaflopsError(Exception):
    """Base exception for all NEXAFLOPS SDK errors."""

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(NexaflopsError):
    """Raised when API key authentication fails.

    Common causes:
    - Invalid API key format
    - Expired API key
    - Revoked API key
    - Missing X-API-Key header
    """

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class LicenseValidationError(NexaflopsError):
    """Raised when license validation fails.

    Attributes:
        license_id: The license ID that failed validation
        reason: Specific reason for failure
    """

    def __init__(
        self,
        message: str,
        license_id: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> None:
        self.license_id = license_id
        self.reason = reason
        super().__init__(message, status_code=403)


class RateLimitError(NexaflopsError):
    """Raised when API rate limit is exceeded.

    Attributes:
        retry_after: Seconds to wait before retrying
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=429)


class NetworkError(NexaflopsError):
    """Raised when a network error occurs.

    Common causes:
    - Connection timeout
    - DNS resolution failure
    - SSL/TLS errors
    - Connection refused
    """

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        self.cause = cause
        super().__init__(message, status_code=None)


class LicenseExpiredError(LicenseValidationError):
    """Raised when attempting to use an expired license."""

    def __init__(self, license_id: str, expired_at: str) -> None:
        super().__init__(
            message=f"License {license_id} expired at {expired_at}",
            license_id=license_id,
            reason="EXPIRED",
        )


class LicenseRevokedError(LicenseValidationError):
    """Raised when attempting to use a revoked license."""

    def __init__(self, license_id: str) -> None:
        super().__init__(
            message=f"License {license_id} has been revoked",
            license_id=license_id,
            reason="REVOKED",
        )


class HostMismatchError(LicenseValidationError):
    """Raised when host fingerprint does not match license binding."""

    def __init__(self, license_id: str) -> None:
        super().__init__(
            message=f"Host fingerprint mismatch for license {license_id}",
            license_id=license_id,
            reason="HOST_MISMATCH",
        )

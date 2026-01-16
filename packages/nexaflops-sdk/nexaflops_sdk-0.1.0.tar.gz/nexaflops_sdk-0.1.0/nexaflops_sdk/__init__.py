"""
NEXAFLOPS SDK - Python client for the NEXAFLOPS Control Plane API.

This SDK provides a simple interface for license validation, management,
and integration with ML training pipelines.

Usage:
    from nexaflops_sdk import NexaflopsClient

    client = NexaflopsClient(api_key="nxf_live_xxx")
    result = client.licenses.validate("license-id", client.get_fingerprint())

    if result.valid:
        # Proceed with training
        pass
"""

from nexaflops_sdk._version import __version__
from nexaflops_sdk.client import NexaflopsClient
from nexaflops_sdk.exceptions import (
    AuthenticationError,
    LicenseValidationError,
    NetworkError,
    NexaflopsError,
    RateLimitError,
)
from nexaflops_sdk.models import (
    License,
    LicenseStatus,
    LicenseTier,
    ValidationResult,
)

__all__ = [
    "NexaflopsClient",
    "NexaflopsError",
    "AuthenticationError",
    "LicenseValidationError",
    "RateLimitError",
    "NetworkError",
    "License",
    "LicenseStatus",
    "LicenseTier",
    "ValidationResult",
    "__version__",
]

"""
Pydantic models for NEXAFLOPS SDK.

These models provide type-safe representations of API responses and requests.
All models use Pydantic v2 for validation and serialization.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LicenseStatus(str, Enum):
    """License status enumeration."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class LicenseTier(str, Enum):
    """License tier enumeration with feature access levels."""

    TRIAL = "TRIAL"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"


class License(BaseModel):
    """Represents a NEXAFLOPS license.

    Attributes:
        id: Unique license identifier (UUID)
        organization_name: Name of the licensed organization
        tier: License tier (TRIAL, PROFESSIONAL, ENTERPRISE)
        status: Current license status
        issued_at: Timestamp when license was issued
        expires_at: Timestamp when license expires
        max_hosts: Maximum number of hosts allowed
        features: Dictionary of enabled features
        limits: Dictionary of usage limits
    """

    id: str = Field(..., description="Unique license identifier")
    organization_name: str = Field(..., description="Licensed organization")
    tier: LicenseTier = Field(..., description="License tier")
    status: LicenseStatus = Field(..., description="Current status")
    issued_at: datetime = Field(..., description="Issue timestamp")
    expires_at: datetime = Field(..., description="Expiry timestamp")
    max_hosts: int = Field(default=1, ge=1, description="Max allowed hosts")
    features: dict = Field(default_factory=dict, description="Enabled features")
    limits: dict[str, int] = Field(default_factory=dict, description="Usage limits")

    @property
    def is_valid(self) -> bool:
        """Check if license is currently valid."""
        now = datetime.now(timezone.utc)
        # Handle naive datetime by assuming UTC
        expires = self.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return self.status == LicenseStatus.ACTIVE and expires > now

    @property
    def days_until_expiry(self) -> int:
        """Get days remaining until license expires."""
        now = datetime.now(timezone.utc)
        expires = self.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        delta = expires - now
        return max(0, delta.days)


class ValidationResult(BaseModel):
    """Result of a license validation request.

    Attributes:
        valid: Whether the license is valid for use
        license_id: The validated license ID
        tier: License tier if valid
        expires_at: Expiry timestamp if valid
        reason: Reason for validation failure (if invalid)
        features: Enabled features for this license
    """

    valid: bool = Field(..., description="Validation result")
    license_id: str = Field(..., description="Validated license ID")
    tier: Optional[LicenseTier] = Field(None, description="License tier")
    expires_at: Optional[datetime] = Field(None, description="Expiry time")
    reason: Optional[str] = Field(None, description="Failure reason")
    features: dict = Field(default_factory=dict, description="Enabled features")

    def raise_if_invalid(self) -> None:
        """Raise LicenseValidationError if validation failed."""
        if not self.valid:
            from nexaflops_sdk.exceptions import LicenseValidationError

            raise LicenseValidationError(
                message=f"License validation failed: {self.reason}",
                license_id=self.license_id,
                reason=self.reason,
            )


class LicenseIssueRequest(BaseModel):
    """Request model for issuing a new license."""

    organization_name: str = Field(..., min_length=1, max_length=255)
    tier: LicenseTier = Field(default=LicenseTier.TRIAL)
    validity_days: int = Field(default=14, ge=1, le=3650)
    max_hosts: int = Field(default=1, ge=1, le=1000)
    features: dict[str, bool] = Field(default_factory=dict)


class PolicyInfo(BaseModel):
    """Public policy information from the Control Plane."""

    public_key: str = Field(..., description="ECDSA public key (Base64)")
    supported_tiers: list[LicenseTier] = Field(
        default_factory=list, description="Available tiers"
    )
    crl_url: Optional[str] = Field(None, description="Certificate Revocation List URL")


class HostFingerprint(BaseModel):
    """Host fingerprint for license binding.

    The fingerprint is a SHA-256 hash of hardware identifiers,
    providing privacy while enabling host verification.
    """

    fingerprint: str = Field(..., description="SHA-256 hash of host info")
    hostname: Optional[str] = Field(None, description="Hostname (optional)")

    @classmethod
    def from_hash(cls, hash_value: str) -> "HostFingerprint":
        """Create fingerprint from pre-computed hash."""
        return cls(fingerprint=hash_value, hostname=None)

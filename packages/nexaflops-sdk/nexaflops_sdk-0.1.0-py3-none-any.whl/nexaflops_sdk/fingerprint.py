"""
Host fingerprinting module for NEXAFLOPS SDK.

This module generates a unique, privacy-preserving fingerprint of the host
machine for license binding. The fingerprint is a SHA-256 hash of hardware
identifiers, ensuring that raw hardware info is never transmitted.

Security Considerations:
- Only hashed values are sent to the Control Plane
- MAC addresses are normalized before hashing
- Hostname is optional to enable container deployments
"""

import hashlib
import platform
import socket
import uuid
from typing import Optional


def get_cpu_info() -> str:
    """Get CPU identifier string.

    Returns a combination of processor name and architecture.
    Falls back to platform info if detailed CPU info is unavailable.
    """
    try:
        processor = platform.processor()
        if processor:
            return processor
    except Exception:
        pass

    # Fallback: use machine type and architecture
    return f"{platform.machine()}-{platform.architecture()[0]}"


def get_primary_mac() -> str:
    """Get the primary network interface MAC address.

    Uses uuid.getnode() which returns a 48-bit positive integer
    representing the hardware address. Format as standard MAC.

    Returns:
        MAC address string in format "XX:XX:XX:XX:XX:XX"
    """
    mac_int = uuid.getnode()
    mac_hex = f"{mac_int:012x}"
    return ":".join(mac_hex[i : i + 2].upper() for i in range(0, 12, 2))


def get_hostname() -> str:
    """Get the current hostname."""
    return socket.gethostname()


def compute_fingerprint(include_hostname: bool = False) -> str:
    """Compute SHA-256 fingerprint of host hardware identifiers.

    The fingerprint is deterministic for the same hardware, enabling
    license binding while preserving privacy (raw values never transmitted).

    Args:
        include_hostname: Whether to include hostname in fingerprint.
                         Set to False for container environments where
                         hostname may change.

    Returns:
        SHA-256 hex digest string (64 characters)
    """
    components = []

    # CPU identifier
    cpu_info = get_cpu_info()
    components.append(f"cpu:{cpu_info}")

    # MAC address (primary NIC)
    mac_addr = get_primary_mac()
    components.append(f"mac:{mac_addr}")

    # Platform info
    os_info = f"{platform.system()}-{platform.release()}"
    components.append(f"os:{os_info}")

    # Optional hostname
    if include_hostname:
        hostname = get_hostname()
        components.append(f"host:{hostname}")

    # Combine and hash
    fingerprint_input = "|".join(sorted(components))
    fingerprint_hash = hashlib.sha256(fingerprint_input.encode("utf-8")).hexdigest()

    return fingerprint_hash


def get_fingerprint_info() -> dict[str, Optional[str]]:
    """Get detailed fingerprint component information.

    This function is useful for debugging fingerprint mismatches.
    The returned values are the raw components (not hashed).

    Returns:
        Dictionary with fingerprint components
    """
    return {
        "cpu": get_cpu_info(),
        "mac": get_primary_mac(),
        "hostname": get_hostname(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "fingerprint": compute_fingerprint(include_hostname=False),
    }


def verify_fingerprint(stored: str, current: Optional[str] = None) -> bool:
    """Verify that current host fingerprint matches stored value.

    Args:
        stored: Previously stored fingerprint (from license)
        current: Current fingerprint (computed if not provided)

    Returns:
        True if fingerprints match, False otherwise
    """
    if current is None:
        current = compute_fingerprint(include_hostname=False)

    # Constant-time comparison to prevent timing attacks
    return _constant_time_compare(stored, current)


def _constant_time_compare(a: str, b: str) -> bool:
    """Compare two strings in constant time.

    Prevents timing attacks by ensuring comparison time does not
    depend on the position of the first difference.
    """
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)

    return result == 0

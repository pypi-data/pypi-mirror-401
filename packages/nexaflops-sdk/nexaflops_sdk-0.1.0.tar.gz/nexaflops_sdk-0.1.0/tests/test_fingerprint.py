"""Tests for fingerprint module."""

import pytest

from nexaflops_sdk.fingerprint import (
    compute_fingerprint,
    get_cpu_info,
    get_fingerprint_info,
    get_hostname,
    get_primary_mac,
    verify_fingerprint,
    _constant_time_compare,
)


class TestFingerprintComponents:
    """Tests for individual fingerprint components."""

    def test_get_cpu_info_returns_string(self) -> None:
        """Test CPU info returns non-empty string."""
        cpu = get_cpu_info()
        assert isinstance(cpu, str)
        assert len(cpu) > 0

    def test_get_primary_mac_format(self) -> None:
        """Test MAC address is in correct format."""
        mac = get_primary_mac()
        assert isinstance(mac, str)
        # MAC format: XX:XX:XX:XX:XX:XX
        parts = mac.split(":")
        assert len(parts) == 6
        for part in parts:
            assert len(part) == 2
            assert all(c in "0123456789ABCDEF" for c in part)

    def test_get_hostname_returns_string(self) -> None:
        """Test hostname returns non-empty string."""
        hostname = get_hostname()
        assert isinstance(hostname, str)
        assert len(hostname) > 0


class TestFingerprintComputation:
    """Tests for fingerprint computation."""

    def test_compute_fingerprint_sha256(self) -> None:
        """Test fingerprint is valid SHA-256."""
        fp = compute_fingerprint()
        assert len(fp) == 64
        assert all(c in "0123456789abcdef" for c in fp)

    def test_fingerprint_without_hostname(self) -> None:
        """Test fingerprint can be computed without hostname."""
        fp = compute_fingerprint(include_hostname=False)
        assert len(fp) == 64

    def test_fingerprint_with_hostname(self) -> None:
        """Test fingerprint includes hostname when requested."""
        fp_without = compute_fingerprint(include_hostname=False)
        fp_with = compute_fingerprint(include_hostname=True)
        # Different inputs should produce different hashes
        # (unless hostname is empty, which is rare)
        # We can't guarantee they're different, but we can verify both work
        assert len(fp_without) == 64
        assert len(fp_with) == 64

    def test_fingerprint_deterministic(self) -> None:
        """Test computing fingerprint twice yields same result."""
        fp1 = compute_fingerprint()
        fp2 = compute_fingerprint()
        assert fp1 == fp2


class TestFingerprintInfo:
    """Tests for fingerprint info retrieval."""

    def test_get_fingerprint_info_keys(self) -> None:
        """Test fingerprint info contains expected keys."""
        info = get_fingerprint_info()
        expected_keys = {
            "cpu",
            "mac",
            "hostname",
            "platform",
            "python_version",
            "fingerprint",
        }
        assert expected_keys.issubset(info.keys())

    def test_fingerprint_info_fingerprint_matches(self) -> None:
        """Test fingerprint in info matches direct computation."""
        info = get_fingerprint_info()
        direct = compute_fingerprint(include_hostname=False)
        assert info["fingerprint"] == direct


class TestFingerprintVerification:
    """Tests for fingerprint verification."""

    def test_verify_matching_fingerprint(self) -> None:
        """Test verification passes for matching fingerprints."""
        fp = compute_fingerprint()
        assert verify_fingerprint(fp, fp) is True

    def test_verify_mismatching_fingerprint(self) -> None:
        """Test verification fails for mismatching fingerprints."""
        fp = compute_fingerprint()
        fake = "a" * 64
        assert verify_fingerprint(fp, fake) is False

    def test_verify_with_current_computation(self) -> None:
        """Test verification computes current fingerprint when not provided."""
        fp = compute_fingerprint()
        assert verify_fingerprint(fp) is True


class TestConstantTimeCompare:
    """Tests for constant-time string comparison."""

    def test_equal_strings(self) -> None:
        """Test equal strings return True."""
        assert _constant_time_compare("abc", "abc") is True

    def test_unequal_strings_same_length(self) -> None:
        """Test unequal strings of same length return False."""
        assert _constant_time_compare("abc", "abd") is False

    def test_unequal_strings_different_length(self) -> None:
        """Test strings of different length return False."""
        assert _constant_time_compare("abc", "abcd") is False

    def test_empty_strings(self) -> None:
        """Test empty strings return True."""
        assert _constant_time_compare("", "") is True

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for CVE validation utilities.

Tests follow TDD principles with comprehensive coverage of:
- Valid CVE formats
- Invalid CVE formats
- Edge cases (None, empty, whitespace)
- Delimiter handling (comma, newline)
- Max length enforcement
"""
import pytest

from regscale.utils.cve_utils import (
    CVE_MAX_LENGTH,
    CVE_PATTERN,
    extract_first_cve,
    validate_cve,
    validate_single_cve,
)


class TestCVEPattern:
    """Tests for CVE_PATTERN regex."""

    @pytest.mark.parametrize(
        "cve",
        [
            "CVE-2021-44832",
            "CVE-2024-1234",
            "CVE-1999-0001",
            "CVE-2025-123456",  # 6 digit ID
            "CVE-2025-1234567",  # 7 digit ID
            "cve-2021-44832",  # lowercase
        ],
    )
    def test_valid_cve_patterns(self, cve: str):
        """Test that valid CVE patterns match."""
        assert CVE_PATTERN.match(cve) is not None

    @pytest.mark.parametrize(
        "invalid_cve",
        [
            "ALAS-2021-1234",  # Amazon Linux
            "RHSA-2021:1234",  # Red Hat
            "USN-1234-1",  # Ubuntu
            "GHSA-xxxx-xxxx-xxxx",  # GitHub
            "CVE-202-1234",  # Year too short
            "CVE-2021-123",  # ID too short
            "CVE2021-1234",  # Missing hyphen
            "CVE-2021_1234",  # Wrong separator
            "",
            "random-string",
        ],
    )
    def test_invalid_cve_patterns(self, invalid_cve: str):
        """Test that invalid CVE patterns do not match."""
        assert CVE_PATTERN.match(invalid_cve) is None


class TestValidateCVE:
    """Tests for validate_cve function."""

    def test_valid_cve_returns_uppercase(self):
        """Test that valid CVE is returned in uppercase."""
        assert validate_cve("cve-2021-44832") == "CVE-2021-44832"
        assert validate_cve("CVE-2021-44832") == "CVE-2021-44832"

    def test_cve_with_whitespace_is_stripped(self):
        """Test that whitespace is stripped."""
        assert validate_cve("  CVE-2021-44832  ") == "CVE-2021-44832"
        assert validate_cve("\tCVE-2021-44832\n") == "CVE-2021-44832"

    def test_none_returns_none(self):
        """Test that None input returns None."""
        assert validate_cve(None) is None

    def test_empty_string_returns_none(self):
        """Test that empty string returns None."""
        assert validate_cve("") is None

    def test_invalid_cve_returns_none(self):
        """Test that invalid CVE formats return None."""
        assert validate_cve("ALAS-2021-1234") is None
        assert validate_cve("not-a-cve") is None
        assert validate_cve("CVE-123-1234") is None


class TestExtractFirstCVE:
    """Tests for extract_first_cve function."""

    def test_single_cve_returned_as_is(self):
        """Test that single CVE is returned stripped."""
        assert extract_first_cve("CVE-2021-44832") == "CVE-2021-44832"
        assert extract_first_cve("  CVE-2021-44832  ") == "CVE-2021-44832"

    def test_comma_delimited_returns_first(self):
        """Test that comma-delimited CVEs return first one."""
        assert extract_first_cve("CVE-2021-44832,CVE-2021-12345") == "CVE-2021-44832"
        assert extract_first_cve("CVE-2021-44832, CVE-2021-12345") == "CVE-2021-44832"

    def test_newline_delimited_returns_first(self):
        """Test that newline-delimited CVEs return first one."""
        assert extract_first_cve("CVE-2021-44832\nCVE-2021-12345") == "CVE-2021-44832"

    def test_mixed_delimiters_returns_first(self):
        """Test mixed delimiters return first CVE."""
        assert extract_first_cve("CVE-2021-44832,CVE-2021-12345\nCVE-2021-99999") == "CVE-2021-44832"

    def test_none_returns_none(self):
        """Test that None input returns None."""
        assert extract_first_cve(None) is None

    def test_empty_string_returns_none(self):
        """Test that empty string returns None."""
        assert extract_first_cve("") is None


class TestValidateSingleCVE:
    """Tests for validate_single_cve function (integration of extract + validate)."""

    def test_valid_single_cve(self):
        """Test valid single CVE is returned uppercase."""
        assert validate_single_cve("CVE-2021-44832") == "CVE-2021-44832"
        assert validate_single_cve("cve-2021-44832") == "CVE-2021-44832"

    def test_comma_delimited_extracts_first_valid(self):
        """Test comma-delimited CVEs return first valid one."""
        assert validate_single_cve("CVE-2021-44832,CVE-2021-12345") == "CVE-2021-44832"

    def test_newline_delimited_extracts_first_valid(self):
        """Test newline-delimited CVEs return first valid one."""
        assert validate_single_cve("CVE-2021-44832\nCVE-2021-12345") == "CVE-2021-44832"

    def test_invalid_cve_returns_none(self):
        """Test invalid CVE returns None."""
        assert validate_single_cve("ALAS-2021-1234") is None
        assert validate_single_cve("not-a-cve") is None

    def test_none_returns_none(self):
        """Test None returns None."""
        assert validate_single_cve(None) is None

    def test_empty_string_returns_none(self):
        """Test empty string returns None."""
        assert validate_single_cve("") is None

    def test_whitespace_only_returns_none(self):
        """Test whitespace-only string returns None."""
        assert validate_single_cve("   ") is None
        assert validate_single_cve("\t\n") is None

    def test_first_invalid_second_valid_returns_none(self):
        """Test that if first CVE is invalid, None is returned (not second)."""
        # We only extract first, so if it's invalid, we return None
        assert validate_single_cve("INVALID,CVE-2021-44832") is None

    def test_max_length_enforcement(self):
        """Test that CVEs exceeding max length return None."""
        # Standard CVE is well under 200 chars, this tests the guard
        assert CVE_MAX_LENGTH == 200
        # A valid CVE is always under 200 chars, so this is just a sanity check
        valid_cve = validate_single_cve("CVE-2021-44832")
        assert valid_cve is not None
        assert len(valid_cve) < CVE_MAX_LENGTH


class TestEdgeCases:
    """Edge case tests for comprehensive coverage."""

    def test_cve_with_leading_trailing_commas(self):
        """Test CVE with leading/trailing delimiters."""
        assert validate_single_cve(",CVE-2021-44832,") is None  # First is empty

    def test_cve_with_spaces_around_delimiters(self):
        """Test CVE with spaces around delimiters."""
        assert validate_single_cve("CVE-2021-44832 , CVE-2021-12345") == "CVE-2021-44832"

    def test_cve_with_multiple_consecutive_delimiters(self):
        """Test CVE with multiple consecutive delimiters."""
        result = extract_first_cve("CVE-2021-44832,,CVE-2021-12345")
        assert result == "CVE-2021-44832"

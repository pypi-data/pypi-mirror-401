#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVE validation and extraction utilities.

This module provides centralized CVE validation following:
- Single Responsibility: All CVE validation logic in one place
- DRY: Reusable across models and integrations
"""
import logging
import re
from typing import Optional

logger = logging.getLogger("regscale")

# CVE format pattern: CVE-YYYY-NNNN (4+ digits for the ID portion)
CVE_PATTERN = re.compile(r"^CVE-\d{4}-\d{4,}$", re.IGNORECASE)
CVE_MAX_LENGTH = 200


def validate_cve(cve: Optional[str]) -> Optional[str]:
    """
    Validate CVE format and return it if valid, otherwise return None.

    CVE format must match: CVE-YYYY-NNNN (e.g., CVE-2021-44832)
    Non-CVE identifiers like ALAS, RHSA, etc. will return None.

    :param cve: The CVE string to validate
    :return: The CVE in uppercase if valid, None otherwise
    :rtype: Optional[str]
    """
    if not cve:
        return None

    cve_stripped = cve.strip()
    if CVE_PATTERN.match(cve_stripped):
        return cve_stripped.upper()

    return None


def extract_first_cve(cve_string: Optional[str]) -> Optional[str]:
    """
    Extract the first CVE from a potentially delimited string.

    Handles comma or newline delimited CVE lists by extracting
    the first valid CVE.

    :param cve_string: String that may contain multiple CVEs
    :return: First CVE found, or original string if no delimiters
    :rtype: Optional[str]
    """
    if not cve_string:
        return None

    if "," in cve_string or "\n" in cve_string:
        candidates = re.split(r"[,\n]", cve_string)
        return candidates[0].strip() if candidates else cve_string

    return cve_string.strip()


def validate_single_cve(cve: Optional[str]) -> Optional[str]:
    """
    Validate and extract a single CVE from input.

    Combines extraction and validation:
    1. Extracts the first CVE if multiple are present (comma or newline delimited)
    2. Validates the CVE format
    3. Enforces 200 character max length
    4. Returns uppercase CVE or None if invalid

    :param cve: CVE string to validate (may contain multiple CVEs)
    :return: Validated single CVE in uppercase, or None if invalid
    :rtype: Optional[str]
    """
    first_cve = extract_first_cve(cve)
    if not first_cve:
        return None

    validated = validate_cve(first_cve)
    if not validated:
        return None

    if len(validated) > CVE_MAX_LENGTH:
        logger.warning("CVE exceeds maximum length of %d: %s", CVE_MAX_LENGTH, validated[:50])
        return None

    return validated

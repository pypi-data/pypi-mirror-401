"""
Qualys Policy Management Integration

This module provides functions to list and export policies from Qualys and import them into RegScale.
"""

import json
import logging
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Any
from urllib.parse import urljoin

from regscale.core.app.utils.app_utils import error_and_exit
from regscale.integrations.integration.policy_upload import PolicyUploader, PolicyUploadRequest

logger = logging.getLogger("regscale")


def _parse_policy_list_response(xml_text: str) -> list:
    """Parse XML policy list response and extract policies."""
    data = ET.fromstring(xml_text)

    # Check for API response code
    response_code = data.find(".//RESPONSE/CODE")
    if response_code is not None and response_code.text != "0":
        error_msg = data.find(".//RESPONSE/TEXT")
        error_text = error_msg.text if error_msg is not None else "Unknown error"
        raise ValueError(f"API error: {error_text}")

    # Extract policy list
    policies = []
    policy_elements = data.findall(".//POLICY_LIST/POLICY")

    for policy_elem in policy_elements:
        policy_dict = {}
        for child in policy_elem:
            policy_dict[child.tag] = child.text
        policies.append(policy_dict)

    return policies


def list_policies() -> list:
    """
    List all policies from Qualys Policy Compliance.

    Returns:
        List of policy dictionaries with: id, title, framework, scope, etc.

    Raises:
        SystemExit: If API request fails
    """
    from regscale.integrations.commercial.qualys import _get_qualys_api

    logger.info("Fetching policy list from Qualys Policy Compliance...")

    base_url, session = _get_qualys_api()

    # Try FO API versions in order: 3.0, 2.0 (2.0 is deprecated but fallback)
    api_versions = ["3.0", "2.0"]
    last_error = None

    for version in api_versions:
        url = urljoin(base_url, f"/api/{version}/fo/compliance/policy/")
        params = {"action": "list"}
        logger.debug("Trying Policy Compliance FO API version %s at %s", version, url)

        try:
            response = session.get(url, params=params)
            response.raise_for_status()

            policies = _parse_policy_list_response(response.text)
            logger.info("Policy Compliance API: Using version %s successfully", version)
            logger.info("Retrieved %s policies from Qualys", len(policies))
            return policies

        except (ValueError, ET.ParseError) as e:
            logger.debug("API version %s failed: %s", version, e)
            last_error = e
            continue

    # All versions failed
    logger.error("Failed to fetch policy list from Qualys using all API versions: %s", last_error)
    error_and_exit(f"Qualys API error: {last_error}")


def _parse_policy_export_response(xml_text: str, policy_id: str) -> dict:
    """Parse XML policy export response and extract policy data."""
    data = ET.fromstring(xml_text)

    # Check for API response code
    response_code = data.find(".//RESPONSE/CODE")
    if response_code is not None and response_code.text != "0":
        error_msg = data.find(".//RESPONSE/TEXT")
        error_text = error_msg.text if error_msg is not None else "Unknown error"
        raise ValueError(f"API error: {error_text}")

    # Extract policy data - convert XML to dict
    policy_dict = {"policyId": policy_id}

    # Get policy metadata
    policy_elem = data.find(".//POLICY")
    if policy_elem is not None:
        for child in policy_elem:
            if child.tag not in ["CONTROLS", "TECHNOLOGIES"]:
                policy_dict[child.tag] = child.text

    # Get controls
    controls = []
    control_elements = data.findall(".//CONTROLS/CONTROL")
    for control_elem in control_elements:
        control_dict = {}
        for child in control_elem:
            control_dict[child.tag] = child.text
        controls.append(control_dict)
    policy_dict["controls"] = controls

    return policy_dict


def export_policy(policy_id: str) -> dict:
    """
    Export a policy from Qualys Policy Compliance.

    Args:
        policy_id: Qualys policy ID

    Returns:
        Policy dict with: id, title, framework, scope, controls, etc.

    Raises:
        SystemExit: If API request fails or policy not found
    """
    from regscale.integrations.commercial.qualys import _get_qualys_api

    logger.info("Exporting policy %s from Qualys Policy Compliance...", policy_id)

    base_url, session = _get_qualys_api()

    # Try FO API versions in order: 3.0, 2.0 (2.0 is deprecated but fallback)
    api_versions = ["3.0", "2.0"]
    last_error = None

    for version in api_versions:
        url = urljoin(base_url, f"/api/{version}/fo/compliance/policy/")
        params = {"action": "export", "id": policy_id}
        logger.debug("Trying Policy Compliance FO API version %s at %s", version, url)

        try:
            response = session.get(url, params=params)
            response.raise_for_status()

            policy_dict = _parse_policy_export_response(response.text, policy_id)
            logger.info("Policy Compliance API: Using version %s successfully", version)
            logger.info("Successfully exported policy: %s", policy_dict.get("TITLE", policy_id))
            return policy_dict

        except (ValueError, ET.ParseError) as e:
            logger.debug("API version %s failed: %s", version, e)
            last_error = e
            continue

    # All versions failed
    logger.error("Failed to export policy %s from Qualys using all API versions: %s", policy_id, last_error)
    error_and_exit(f"Qualys API error: {last_error}")


def convert_qualys_policy_to_regscale(
    qualys_policy: dict,
    parent_id: int,
    parent_module: str,
    policy_type: Optional[str] = None,
    status: str = "Active",
) -> PolicyUploadRequest:
    """
    Convert Qualys policy dict to RegScale PolicyUploadRequest.

    Args:
        qualys_policy: Policy dict from export_policy()
        parent_id: RegScale Security Plan or Component ID
        parent_module: "securityplans" or "components"
        policy_type: Override policy type (optional)
        status: Policy status (default: "Active")

    Returns:
        PolicyUploadRequest object ready to upload to RegScale
    """
    # Extract policy metadata (may be nested under "policy" key from export)
    policy_metadata = qualys_policy.get("policy", qualys_policy)

    # Build description from framework, scope, and controls
    description_parts = []

    # Add framework and scope information
    if policy_metadata.get("framework"):
        description_parts.append(f"**Framework**: {policy_metadata['framework']}")

    if policy_metadata.get("scope"):
        description_parts.append(f"**Scope**: {policy_metadata['scope']}")

    if policy_metadata.get("description"):
        description_parts.append(f"\n{policy_metadata['description']}")

    # Add controls summary if present
    controls = qualys_policy.get("controls", [])
    if controls:
        description_parts.append(f"\n\n**Controls**: {len(controls)} control(s) defined")

    description = "\n\n".join(description_parts) if description_parts else "No description available"

    # Create PolicyUploadRequest using the centralized policy upload module
    # The PolicyUploader will handle date formatting and owner ID automatically
    request = PolicyUploadRequest(
        policy_number=f"QUALYS-PC-{policy_metadata.get('policyId', '')}",
        title=policy_metadata.get("policyName", "Untitled Policy"),
        description=description,
        policy_type=policy_type or policy_metadata.get("framework", "Custom"),
        status=status,
        parent_module=parent_module,
        parent_id=parent_id,
    )

    return request


def save_policy_to_file(policy: dict, filepath: str) -> None:
    """
    Save policy dict to JSON file.

    Args:
        policy: Policy dictionary
        filepath: Output file path

    Raises:
        IOError: If file write fails
    """
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(policy, f, indent=2, ensure_ascii=False)
        logger.info("Policy saved to: %s", filepath)
    except IOError as e:
        logger.error("Failed to save policy to file: %s", e)
        raise


def load_policy_from_file(filepath: str) -> dict:
    """
    Load policy dict from JSON file.

    Args:
        filepath: Input file path

    Returns:
        Policy dictionary

    Raises:
        IOError: If file read fails
        json.JSONDecodeError: If JSON parsing fails
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            policy = json.load(f)
        logger.info("Policy loaded from: %s", filepath)
        return policy
    except (IOError, json.JSONDecodeError) as e:
        logger.error("Failed to load policy from file: %s", e)
        raise

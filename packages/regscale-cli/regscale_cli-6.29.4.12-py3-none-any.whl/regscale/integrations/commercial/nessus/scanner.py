"""
Scanner integration for Nessus vulnerability scanning.
"""

import logging
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union, cast
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree

import nessus_file_reader as nfr  # type: ignore

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.core.app.utils.file_utils import find_files, get_processed_file_path, iterate_files, move_file, read_file
from regscale.core.app.utils.parser_utils import safe_float
from regscale.core.utils.date import date_str
from regscale.integrations.commercial.nessus.nessus_utils import cpe_xml_to_dict, software
from regscale.integrations.scanner_integration import IntegrationAsset, IntegrationFinding, ScannerIntegration
from regscale.integrations.variables import ScannerVariables
from regscale.models import ImportValidater, regscale_models
from regscale.validation.address import validate_ip_address

logger = logging.getLogger("regscale")


class NessusIntegration(ScannerIntegration):
    """Integration class for Nessus vulnerability scanning."""

    title = "Nessus"
    asset_identifier_field = "otherTrackingNumber"  # Must be valid batch API UniqueKeyField
    finding_severity_map = {
        "4": regscale_models.IssueSeverity.Critical,
        "3": regscale_models.IssueSeverity.High,
        "2": regscale_models.IssueSeverity.Moderate,
        "1": regscale_models.IssueSeverity.Low,
        "critical": regscale_models.IssueSeverity.Critical,
        "high": regscale_models.IssueSeverity.High,
        "medium": regscale_models.IssueSeverity.Moderate,
        "low": regscale_models.IssueSeverity.Low,
    }

    @staticmethod
    def log_file_warning_and_exit(path: str, exit_app: bool = True) -> None:
        """
        Log a warning message stating that the Nessus file was not found.

        :param str path: The path to the Nessus file that was not found
        :param bool exit_app: Whether to exit the program after logging the warning, defaults to True
        :rtype: None
        """
        logger.warning("No Nessus files found in path %s", path)
        if exit_app:
            sys.exit(0)

    @staticmethod
    def _check_path(path: Optional[str] = None) -> None:
        """
        Check if the path is a valid Nessus file path.

        :param Optional[str] path: The path to check, defaults to None
        :raises ValueError: If the path is provided path is not provided
        :rtype: None
        """
        if not path:
            raise ValueError("Nessus file path must end with .nessus")

    @staticmethod
    def _get_host_ip(root: Any, asset_name: str) -> str:
        """
        Extract the host IP address from Nessus XML HostProperties.

        :param root: The Nessus root element
        :param str asset_name: The asset name from ReportHost
        :return: The IP address or empty string if not found/invalid
        :rtype: str
        """
        xpath = "./Report/ReportHost[@name='%s']/HostProperties/tag[@name='host-ip']" % asset_name
        tag = root.find(xpath)
        if tag is not None and tag.text:
            ip_value = tag.text.strip()
            if validate_ip_address(ip_value):
                return ip_value
        return ""

    def fetch_findings(self, *args: Tuple, **kwargs: dict) -> Iterator[IntegrationFinding]:
        """
        Fetches Nessus findings from the processed Nessus files.

        Creates a separate finding for each CVE associated with a vulnerability.
        If a vulnerability has multiple CVEs, multiple findings are yielded.

        :return: Iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        path: Optional[str] = cast(Optional[str], kwargs.get("path"))
        self._check_path(path)
        file_collection = find_files(path, "*.nessus")
        if not file_collection:
            self.log_file_warning_and_exit(path)
        if not self.check_collection(file_collection, path):
            return
        self.num_findings_to_process = 0
        for file in iterate_files(file_collection):
            yield from self._process_nessus_file(file)
        self.move_files(file_collection)

    def _process_nessus_file(self, file: Union[Path, str]) -> Iterator[IntegrationFinding]:
        """
        Process a single Nessus file and yield findings.

        :param file: Path to the Nessus file
        :return: Iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        content = read_file(file)
        root = ET.fromstring(content)
        scan_dt = nfr.scan.scan_time_start(root)
        if scan_dt:
            self.scan_date = scan_dt.strftime("%Y-%m-%d")
        for nessus_asset in nfr.scan.report_hosts(root):
            asset_name = nfr.host.report_host_name(nessus_asset)
            host_ip = self._get_host_ip(root, asset_name)
            yield from self._process_asset_vulnerabilities(root, asset_name, host_ip)

    def _process_asset_vulnerabilities(self, root: Any, asset_name: str, host_ip: str) -> Iterator[IntegrationFinding]:
        """
        Process all vulnerabilities for a single asset.

        :param root: The XML root element
        :param str asset_name: The asset name/identifier
        :param str host_ip: The validated IP address of the host
        :return: Iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        xpath = "./Report/ReportHost[@name='%s']/ReportItem" % asset_name
        for vuln in root.iterfind(xpath):
            yield from self._yield_findings_for_vulnerability(vuln, asset_name, host_ip)

    def _yield_findings_for_vulnerability(
        self, vuln: Any, asset_name: str, host_ip: str
    ) -> Iterator[IntegrationFinding]:
        """
        Yield findings for a single vulnerability, creating one finding per CVE.

        :param vuln: The vulnerability XML element
        :param str asset_name: The asset name/identifier
        :param str host_ip: The validated IP address of the host
        :return: Iterator of IntegrationFinding objects
        :rtype: Iterator[IntegrationFinding]
        """
        cves = [el.text for el in vuln.findall("cve") if el.text]
        unique_cves = list(set(cves))
        if unique_cves:
            # Create one finding per unique CVE
            for cve in unique_cves:
                parsed = self.parse_finding(vuln, asset_name, cve=cve, host_ip=host_ip)
                if parsed:
                    self.num_findings_to_process += 1
                    yield parsed
        else:
            # No CVEs - create single finding without CVE
            parsed = self.parse_finding(vuln, asset_name, cve=None, host_ip=host_ip)
            if parsed:
                self.num_findings_to_process += 1
                yield parsed

    def parse_finding(
        self, vuln: Any, asset_id: str, cve: Optional[str] = None, host_ip: str = ""
    ) -> Optional[IntegrationFinding]:
        """
        Parses a Nessus vulnerability or informational item into an IntegrationFinding object.

        :param Any vuln: The Nessus vulnerability or informational item to parse
        :param str asset_id: The asset identifier
        :param Optional[str] cve: The specific CVE for this finding (one finding per CVE)
        :param str host_ip: The validated IP address of the host
        :return: The parsed IntegrationFinding or None if parsing fails
        :rtype: Optional[IntegrationFinding]
        """
        try:
            vulnerability_data = self.get_vulnerability_data(vuln)
            if hasattr(vuln, "attrib"):
                vuln = vuln.attrib
            vuln.update(vulnerability_data)

            # Determine if this is an informational item or a vulnerability
            is_informational = vuln.get("severity") == "0" and vuln.get("risk_factor", "").lower() == "none"

            if is_informational:
                return None

            category = f"Nessus Vulnerability: {vuln.get('pluginFamily', 'General')}"
            issue_type = "Vulnerability"
            severity = self.finding_severity_map.get(vuln["severity"].lower(), regscale_models.IssueSeverity.Low)
            status = regscale_models.IssueStatus.Open

            synopsis = vuln.get("synopsis", "")
            plugin_name = vuln.get("pluginName", "Unknown Plugin")
            plugin_id = vuln.get("pluginID", "Unknown")

            # Get severity_int, defaulting to 0 if not found
            severity_int = int(vuln.get("severity", "0"))
            identifier = cve or plugin_name

            # Create unique external_id: include CVE when present for deduplication
            external_id = "%s_%s" % (plugin_id, cve) if cve else plugin_id

            return IntegrationFinding(
                control_labels=[],
                category=category,
                title="%s: %s" % (identifier, synopsis),
                issue_title="%s: %s" % (identifier, synopsis),
                description=vuln.get("description"),
                severity=severity or regscale_models.IssueSeverity.Low,
                status=status,
                asset_identifier=asset_id,
                external_id=external_id,
                first_seen=vuln.get("firstSeen") or get_current_datetime(),
                last_seen=vuln.get("lastSeen") or get_current_datetime(),
                remediation=vuln.get("solution", ""),
                cvss_score=float(vuln.get("cvss_base_score") or 0),
                cve=cve,  # Single CVE per finding
                vulnerability_type=self.title,
                plugin_id=plugin_id,
                plugin_name=identifier,
                ip_address=host_ip,
                dns=None,
                severity_int=severity_int,
                issue_type=issue_type,
                date_created=get_current_datetime(),
                date_last_updated=get_current_datetime(),
                gaps="",
                observations=vuln.get("plugin_output", ""),
                evidence=vuln.get("plugin_output", ""),
                identified_risk=vuln.get("risk_factor", ""),
                impact="",
                recommendation_for_mitigation=vuln.get("solution", ""),
                rule_id=plugin_id,
                rule_version=vuln.get("script_version"),
                results=vuln.get("plugin_output", ""),
                comments=None,
                baseline="",
                poam_comments=None,
                vulnerable_asset=asset_id,
                source_rule_id=vuln.get("fname"),
            )
        except Exception as e:
            logger.error("Error parsing Nessus finding: %s", str(e), exc_info=True)
            return None

    def check_collection(self, file_collection: List[Union[Path, str]], path: str) -> bool:
        """
        Check if any Nessus files were found in the given path.

        :param List[Union[Path, str]] file_collection: List of Path objects for .nessus files or S3 URIs
        :param str path: Path to a .nessus file or a folder containing Nessus files
        :return: boolean indicating if any Nessus files were found
        :rtype: bool
        """
        res = True
        if len(file_collection) == 0:
            self.log_file_warning_and_exit(path, exit_app=False)
            res = False
        return res

    def fetch_assets(self, *args: Any, **kwargs: dict) -> Iterator[IntegrationAsset]:  # type: ignore
        """
        Fetches Nessus assets from the processed Nessus files.

        :param str path: Path to the Nessus files
        :yields: Iterator[IntegrationAsset]
        """
        path: Optional[str] = cast(Optional[str], kwargs.get("path"))

        file_collection = find_files(path, "*.nessus")
        if not file_collection:
            self.log_file_warning_and_exit(path)
        if self.check_collection(file_collection, path):
            for file in iterate_files(file_collection):
                ImportValidater(
                    file_path=file,
                    disable_mapping=True,
                    required_headers=["Policy", "Report"],
                    mapping_file_path=tempfile.gettempdir(),
                    xml_tag="NessusClientData_v2",
                    prompt=False,
                )
                content = read_file(file)
                root = ET.fromstring(content)
                tree = ElementTree(root)
                assets = nfr.scan.report_hosts(root)
                cpe_items = cpe_xml_to_dict(tree)  # type: ignore
                self.num_assets_to_process = len(assets)
                for asset in assets:
                    asset_properties = self.get_asset_properties(root, cpe_items, asset)
                    parsed_asset = self.parse_asset(asset_properties)
                    yield parsed_asset

    def parse_asset(self, asset: Dict[str, Any]) -> IntegrationAsset:
        """
        Parses Nessus assets.

        :param Dict[str, Any] asset: The Nessus asset to parse
        :return: The parsed IntegrationAsset
        :rtype: IntegrationAsset
        """
        software_inventory = [
            {
                "name": software_obj.get("title"),
                "version": software_obj.get("version"),
                "references": software_obj.get("references", []),
            }
            for software_obj in asset.get("software_inventory", [])
        ]

        return IntegrationAsset(
            name=asset.get("name", ""),
            identifier=asset.get("name")
            or asset.get("host_ip", "")
            or asset.get("fqdn", "")
            or asset.get("tenable_id", ""),
            asset_type=asset.get("asset_type", "Other"),
            asset_category=regscale_models.AssetCategory.Hardware,
            asset_owner_id=ScannerVariables.userId,
            parent_id=self.plan_id,
            parent_module=regscale_models.SecurityPlan.get_module_slug(),
            status=asset.get("status", "Active (On Network)"),
            date_last_updated=date_str(asset.get("last_scan") or get_current_datetime()),
            mac_address=asset.get("mac_address", ""),
            fqdn=asset.get("fqdn", ""),
            ip_address=asset.get("host_ip", ""),
            operating_system=asset.get("operating_system", ""),
            aws_identifier=asset.get("aws_identifier", ""),
            vlan_id=asset.get("vlan_id", ""),
            location=asset.get("location", ""),
            software_inventory=software_inventory,
        )

    @staticmethod
    def _get_tag_mapping() -> Dict[str, str]:
        """
        Get the mapping of Nessus tag names to asset property names.

        :return: Dictionary mapping Nessus tag names to property names
        :rtype: Dict[str, str]
        """
        return {
            "id": "tenable_id",
            "host-ip": "host_ip",
            "host-fqdn": "fqdn",
            "mac-address": "macaddress",
            "HOST_START_TIMESTAMP": "begin_scan",
            "HOST_END_TIMESTAMP": "last_scan",
            "aws-instance-instanceId": "aws_instance_id",
            "aws-instance-vpc-id": "vlan_id",
            "aws-instance-region": "location",
        }

    @staticmethod
    def _extract_tag_values(root: Any, xpath: str, tag_map: Dict[str, str]) -> Dict[str, str]:
        """
        Extract tag values from XML based on tag mapping.

        :param root: The Nessus root element
        :param str xpath: XPath to find tags
        :param Dict[str, str] tag_map: Mapping of tag names to property names
        :return: Dictionary of extracted tag values
        :rtype: Dict[str, str]
        """
        tag_values = dict.fromkeys(tag_map.values(), "")
        for file_asset_tag in root.iterfind(xpath):
            tag_name = file_asset_tag.attrib.get("name")
            if tag_name in tag_map:
                variable_name = tag_map[tag_name]
                tag_values[variable_name] = file_asset_tag.text or ""
        return tag_values

    @staticmethod
    def _build_all_tags(root: Any, xpath: str) -> List[Dict[str, Any]]:
        """
        Build list of all tags from XML.

        :param root: The Nessus root element
        :param str xpath: XPath to find tags
        :return: List of tag dictionaries
        :rtype: List[Dict[str, Any]]
        """
        return [{"name": attrib.attrib["name"], "val": attrib.text} for attrib in root.iterfind(xpath)]

    @staticmethod
    def _extract_basic_asset_info(root: Any, file_asset: Any) -> Dict[str, Any]:
        """
        Extract basic asset information from Nessus data.

        :param root: The Nessus root element
        :param file_asset: The file asset
        :return: Dictionary of basic asset information
        :rtype: Dict[str, Any]
        """
        return {
            "nessus_report_uuid": nfr.scan.server_preference_value(root, "report_task_id"),
            "asset_name": nfr.host.report_host_name(file_asset),
            "operating_system": nfr.host.detected_os(file_asset),
            "netbios": nfr.host.netbios_network_name(root, file_asset),
            "resolved_ip": nfr.host.resolved_ip(file_asset),
            "scanner_ip": nfr.host.scanner_ip(root, file_asset),
            "asset_count": len(list(root.iter("ReportHost"))),
        }

    @classmethod
    def get_asset_properties(cls, root, cpe_items, file_asset) -> dict:
        """
        Get the asset properties

        :param root: The Nessus root element
        :param cpe_items: The CPE items
        :param file_asset: The file asset
        :return: dict of asset properties
        :rtype: dict
        """
        basic_info = cls._extract_basic_asset_info(root, file_asset)
        asset_name = basic_info["asset_name"]
        xpath = f"./Report/ReportHost[@name='{asset_name}']/HostProperties/tag"

        tag_map = cls._get_tag_mapping()
        tag_values = cls._extract_tag_values(root, xpath, tag_map)
        all_tags = cls._build_all_tags(root, xpath)
        software_inventory = software(cpe_items, file_asset)

        return {
            "name": asset_name,
            "operating_system": basic_info["operating_system"],
            "tenable_id": tag_values.get("tenable_id", ""),
            "netbios_name": basic_info["netbios"]["netbios_computer_name"],
            "all_tags": all_tags,
            "mac_address": tag_values["macaddress"],
            "last_scan": tag_values["last_scan"],
            "resolved_ip": basic_info["resolved_ip"],
            "asset_count": basic_info["asset_count"],
            "scanner_ip": basic_info["scanner_ip"],
            "host_ip": tag_values["host_ip"],
            "fqdn": tag_values["fqdn"],
            "software_inventory": software_inventory,
            "nessus_report_uuid": basic_info["nessus_report_uuid"],
            "aws_identifier": tag_values["aws_instance_id"],
            "vlan_id": tag_values["vlan_id"],
            "location": tag_values["location"],
        }

    @classmethod
    def all_element_data(cls, element: Any, indent: str = "") -> str:
        """
        Recursively walk down the XML element and return a string representation.

        :param Any element: A file vulnerability XML element
        :param str indent: Current indentation level (for pretty printing)
        :return: String representation of the vulnerability data
        :rtype: str
        """
        result = []

        if element.text and element.text.strip():
            result.append(f"{indent}{element.tag}: {element.text.strip()}")

        for attr, value in element.attrib.items():
            result.append(f"{indent}{element.tag}.{attr}: {value}")

        for child in element:
            result.append(cls.all_element_data(child, indent + "  "))

        return "\n".join(result)

    @classmethod
    def get_vulnerability_data(cls, file_vuln: Any) -> dict:
        """
        Get the vulnerability data from a Nessus XML element.

        :param Any file_vuln: A file vulnerability XML element
        :return: dict of vulnerability data
        :rtype: dict
        """

        def get(field_name: str) -> Optional[str]:
            """
            Get the field value from the XML element.

            :param str field_name: The field name to get
            :return: Field value
            :rtype: Optional[str]
            """
            element = file_vuln.find(field_name)
            return element.text if element is not None else None

        def get_all(field_name: str) -> List[str]:
            """
            Get all field values from the XML element.

            :param str field_name: The field name to get
            :return: List of field values
            :rtype: List[str]
            """
            elements = file_vuln.findall(field_name)
            return [el.text for el in elements if el.text]

        def get_attrib(attr_name: str) -> Optional[str]:
            """
            Get the attribute value from the XML element.

            :param str attr_name: The attribute name to get
            :return: Attribute value
            :rtype: Optional[str]
            """
            return file_vuln.get(attr_name)

        description = get("description")
        plugin_output = get("plugin_output")
        cvss_base_score = safe_float(get("cvss3_base_score"))
        cves = get_all("cve")  # Get ALL CVEs, not just the first one
        synopsis = get("synopsis")
        solution = get("solution")
        severity = get_attrib("severity")
        plugin_id = get_attrib("pluginID")
        plugin_name = get_attrib("pluginName")
        risk_factor = get("risk_factor")
        script_version = get("script_version")
        fname = get("fname")

        return {
            "description": description,
            "synopsis": synopsis,
            "plugin_output": plugin_output,
            "cves": cves,  # List of all CVEs
            "cvss_base_score": cvss_base_score,
            "severity": severity,
            "solution": solution,
            "pluginID": plugin_id,
            "pluginName": plugin_name,
            "risk_factor": risk_factor,
            "script_version": script_version,
            "fname": fname,
        }

    @staticmethod
    def move_files(file_collection: List[Union[Path, str]]) -> None:
        """
        Move the list of files to a folder called 'processed' in the same directory.

        :param List[Union[Path, str]] file_collection: List of file paths or S3 URIs
        :return: None
        :rtype: None
        """
        for file in file_collection:
            new_file = get_processed_file_path(file)
            move_file(file, new_file)
            logger.info("Moved Nessus file %s to %s", file, new_file)

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model for a RegScale File"""

# flake8: noqa
# standard python imports
import gzip
import logging
import mimetypes
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field
from requests import JSONDecodeError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import (
    compute_hash,
    error_and_exit,
    get_current_datetime,
    get_file_name,
    get_file_type,
)
from regscale.models.regscale_models.tag import Tag
from regscale.models.regscale_models.tag_mapping import TagMapping

logger = logging.getLogger(__name__)


class File(BaseModel):
    """File Model"""

    model_config = ConfigDict(populate_by_name=True)

    # fileHash and shaHash are not required because this is due
    # fileHash is the old method and shaHash is the new method in RegScale
    # We are not sure which one will be used/returned
    id: str
    trustedDisplayName: str
    trustedStorageName: str
    size: int
    fullPath: str
    mimeType: Optional[str] = ""
    partType: Optional[str] = ""
    partId: Optional[str] = ""
    folder: Optional[str] = ""
    uploadedById: Optional[str] = None
    uploadDate: str = Field(default_factory=get_current_datetime, alias="uploadedDate")
    fileName: Optional[str] = Field("", alias="file_name")
    fileHash: Optional[str] = None
    shaHash: Optional[str] = None
    parentId: int = 0
    parentModule: str = ""
    tags: Optional[str] = ""

    @staticmethod
    def download_file_from_regscale_to_memory(
        api: Api, record_id: int, module: str, stored_name: str, file_hash: str
    ) -> Optional[bytes]:
        """
        Download a file from RegScale

        :param Api api: API object
        :param int record_id: RegScale record ID
        :param str module: RegScale module
        :param str stored_name: RegScale stored name
        :param str file_hash: RegScale file hash
        :return: Bytes of file as BytesIO object, or None if download failed
        :rtype: Optional[bytes]
        """
        response = api.get(
            url=f'{api.config["domain"]}/api/files/downloadFile/{record_id}/{module}/{stored_name}/{file_hash}'
        )
        if response is None:
            logger.warning("Failed to download file from RegScale: No response received")
            return None
        if not response.ok:
            logger.warning(
                "Failed to download file from RegScale: %s %s",
                response.status_code,
                response.reason,
            )
            return None

        content = response.content
        # Validate that the response is not an error page
        if File._is_error_response(content, stored_name):
            return None
        return content

    @staticmethod
    def _is_error_response(content: bytes, filename: str) -> bool:
        """
        Check if downloaded content is an error response instead of actual file data.

        :param bytes content: The downloaded content
        :param str filename: The filename for logging purposes
        :return: True if content appears to be an error response
        :rtype: bool
        """
        if not content or len(content) == 0:
            logger.warning("Downloaded empty content for file '%s'", filename)
            return True

        # Check first bytes for error patterns
        try:
            # Get first 100 bytes as string for pattern matching
            header = content[:100].decode("utf-8", errors="ignore").lower()
        except Exception:
            # If we can't decode, it's likely binary data (which is fine)
            return False

        # Check for HTML error pages
        if header.startswith("<!doctype") or header.startswith("<html") or header.startswith("<?xml"):
            logger.warning(
                "Downloaded content for '%s' appears to be an HTML/XML error page, not file data",
                filename,
            )
            return True

        # Check for JSON error responses
        if header.startswith('{"error') or header.startswith('{"status":"error'):
            logger.warning(
                "Downloaded content for '%s' appears to be a JSON error response, not file data",
                filename,
            )
            return True

        # Check for common error message patterns (quoted strings often indicate error text)
        error_patterns = ['"unable', '"error', '"failed', '"not found', '"access denied']
        if any(header.startswith(pattern) for pattern in error_patterns):
            logger.warning(
                "Downloaded content for '%s' appears to be an error message, not file data",
                filename,
            )
            return True

        # Check if file claims to be binary (image, etc.) but contains ASCII text
        file_ext = Path(filename).suffix.lower()
        binary_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico", ".webp", ".pdf", ".zip", ".gz", ".tar"}
        if file_ext in binary_extensions:
            # Check if content starts with a quote (text) instead of binary magic bytes
            if header.startswith('"') or header.startswith("'"):
                logger.warning(
                    "Downloaded content for '%s' appears to be text, not binary data (expected %s)",
                    filename,
                    file_ext,
                )
                return True
            # Check for suspiciously small image files (real images are almost always > 500 bytes)
            if file_ext in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"} and len(content) < 500:
                logger.warning(
                    "Downloaded content for '%s' is too small (%d bytes) to be a valid image",
                    filename,
                    len(content),
                )
                return True

        return False

    @staticmethod
    def get_files_for_parent_from_regscale(
        parent_id: int, parent_module: str, api: Optional[Api] = None
    ) -> list["File"]:
        """
        Function to download all files from RegScale for the provided parent ID and module

        :param int parent_id: RegScale parent ID
        :param str parent_module: RegScale module
        :param Optional[Api] api: API object
        :return: List of File objects
        :rtype: list[File]
        """
        if not api:
            api = Api()
        # get the files from RegScale
        files = []
        try:
            file_response = api.get(url=f"{api.config['domain']}/api/files/{parent_id}/{parent_module}").json()
            files = [File(**file) for file in file_response]
        except JSONDecodeError:
            api.logger.error("Unable to retrieve files from RegScale for the provided ID & module.")
        except Exception as ex:
            error_and_exit(f"Unable to retrieve files from RegScale.\n{ex}")
        return files

    @staticmethod
    def delete_file(app: Application, file: "File") -> bool:
        """
        Delete a file from RegScale

        :param Application app: Application Instance
        :param File file: File to delete in RegScale
        :return: Whether the file was deleted
        :rtype: bool
        """
        api = Api()

        response = api.delete(app.config["domain"] + f"/api/files/{file.id}")
        return response.ok

    @staticmethod
    def _log_upload_rejection(api: Api, file_name: str, regscale_file: dict) -> None:
        """Log appropriate warning message when file upload is rejected."""
        file_display_name = Path(file_name).name
        if "error" in regscale_file:
            api.logger.warning("Skipping file '%s' - %s", file_display_name, regscale_file["error"])
            return
        ext = Path(file_name).suffix
        if not ext:
            api.logger.warning("Skipping file '%s' - RegScale requires files to have extensions.", file_display_name)
        else:
            api.logger.warning(
                "Skipping file '%s' - server rejected upload (check admin file configuration).", file_display_name
            )

    @staticmethod
    def upload_file_to_regscale(
        file_name: str,
        parent_id: int,
        parent_module: str,
        api: Api,
        file_data: Optional[Union[bytes, dict, bool]] = None,
        return_object: Optional[bool] = False,
        tags: Optional[str] = None,
    ) -> Optional[Union[bytes, dict, bool]]:
        """
        Function that will create and upload a file to RegScale to the provided parent_module and parent_id
        returns whether the file upload was successful or not

        :param str file_name: Path to the file to upload
        :param int parent_id: RegScale parent ID
        :param str parent_module: RegScale module
        :param Api api: API object
        :param Optional[Union[bytes, dict, bool]] file_data: File data to upload, defaults to None
        :param Optional[bool] return_object: Whether to return the file object from RegScale, defaults to False
        :param Optional[str] tags: Tags to add to the file, defaults to None
        :return: Boolean indicating whether the file upload was successful or not
        :rtype: Optional[bytes, dict, bool]
        """
        regscale_file = File._create_regscale_file(
            file_path=file_name,
            parent_id=parent_id,
            parent_module=parent_module,
            api=api,
            file_data=file_data,
        )
        if not regscale_file:
            return False

        if "id" not in regscale_file:
            File._log_upload_rejection(api, file_name, regscale_file)
            return False

        mime_type = File.determine_mime_type(Path(file_name).suffix)
        if not mime_type:
            return False

        file_headers = {
            "Authorization": api.config["token"],
            "accept": "application/json, text/plain, */*",
        }
        new_file = File(
            parentId=parent_id,
            tags=tags,
            parentModule=parent_module,
            uploadedById=api.config["userId"],
            mimeType=mime_type,
            id=regscale_file["id"],
            fullPath=regscale_file["fullPath"],
            trustedDisplayName=regscale_file["trustedDisplayName"],
            trustedStorageName=regscale_file["trustedStorageName"],
            uploadDate=regscale_file["uploadDate"],
            fileHash=regscale_file["fileHash"],
            shaHash=regscale_file["shaHash"],
            size=(sys.getsizeof(file_data) if file_data else regscale_file["size"]),
        )
        file_res = api.post(
            url=f"{api.config['domain']}/api/files",
            headers=file_headers,
            json=new_file.model_dump(),
        )
        if file_res.ok and return_object:
            return File(**file_res.json()).model_dump()
        File.create_tag_mappings(file_res)
        return file_res.ok

    @staticmethod
    def get_existing_tags_dict() -> dict:
        """Fetch existing tags and return a dictionary mapping tag titles to their IDs.
        :return: Dictionary mapping tag titles to their IDs
        :rtype: dict
        """
        existing_tag_list = Tag.get_list()
        return {tag.title: tag.id for tag in existing_tag_list}

    @staticmethod
    def process_tag(tag: str, file_id: str, tags_dict: dict):
        """Process a single tag and create a TagMapping if the tag exists.
        :param str tag: The tag to process
        :param str file_id: The file uuid
        :param dict tags_dict: The dictionary mapping tag titles to their IDs
        """
        tag_id = tags_dict.get(tag)
        if tag_id:
            tag_mapping = TagMapping(parentId=file_id, parentModule="files", tagId=tag_id)
            tag_mapping.create()

    @staticmethod
    def create_tag_mappings(file_res: any):
        """Create tag mappings for the given file response.
        :param any file_res: The file response from RegScale
        """
        if file_id := file_res.json().get("id"):
            tags_dict = File.get_existing_tags_dict()
            tags = file_res.json().get("tags", "")
            for tag in tags.replace(" ", "").split(","):
                File.process_tag(tag, file_id, tags_dict)

    @staticmethod
    def _check_compression(
        size_limit_mb: int = 25, file_path: str = None, file_data: Optional[bytes] = None
    ) -> Tuple[str, float]:
        """
        Function to check if the file should be auto compressed.

        :param int size_limit_mb: The size limit in MB, defaults to 25
        :param str file_path: The file path, defaults to None
        :param Optional[bytes] file_data: File data to calculate size from, defaults to None
        :return: The file path
        :rtype: Tuple[str, float]
        """
        app = Application()
        try:
            size = os.path.getsize(file_path)  # kb
        except FileNotFoundError:
            # get size from file_data
            size = sys.getsizeof(file_data)  # bytes
            # convert bytes to kb
            return file_path, size / 1024
        app.logger.debug("File size: %i MB", size_limit_mb)
        if size > size_limit_mb * 1024 * 1024:
            app.logger.warning("The file is over %i MB. It will be compressed.", size_limit_mb)
            # compress the file
            output_path = Path(file_path).parent / Path(file_path).with_suffix(".gz").name
            file_path = File._compress_file(file_path, output_path)
            size = os.path.getsize(file_path)
        return file_path, size

    @staticmethod
    def _compress_file(input_file_path: Union[Path, str], output_file_path: Union[Path, str]) -> str:
        """
        Function to compress a file using gzip

        :param Union[Path, str] input_file_path: The input file path
        :param Union[Path, str] output_file_path: The output file path
        :return: The output file path
        :rtype: str
        """
        with open(input_file_path, "rb") as f_in:
            # Max compression
            with gzip.GzipFile(filename=output_file_path, mode="wb", compresslevel=9) as f_out:
                f_out.write(f_in.read())
        return str(output_file_path)

    @staticmethod
    def _create_regscale_file(
        file_path: str,
        parent_id: int,
        parent_module: str,
        api: Api,
        file_data: Optional[bytes] = None,
    ) -> Optional[dict]:
        """
        Function to create a file within RegScale via API
        :param str file_path: Path to the file
        :param int parent_id: RegScale parent ID
        :param str parent_module: RegScale module
        :param Api api: API object
        :param Optional[bytes] file_data: File data to upload, defaults to None
        :raises: General error if unacceptable file type was provided
        :return: Dictionary of the file object from RegScale or None
        :rtype: Optional[dict]
        """

        # check if the file should be auto compressed
        file_path, file_size = File._check_compression(file_path=file_path, size_limit_mb=100, file_data=file_data)

        # get the file type of the provided file_path
        file_type = get_file_type(file_path)

        # get the file name from the provided file_path
        file_name = get_file_name(file_path)

        if file_size == 0:
            raise ValueError("File size is 0 bytes")

        if file_size > 104857600:
            mb_size = file_size / 1024 / 1024
            limit_size = 104857600 / 1024 / 1024  # 100 MB
            raise ValueError(f"File size is {mb_size} MB. This is over the max file size of {limit_size} MB")

        # set up file headers
        file_headers = {
            "Authorization": api.config["token"],
            "Accept": "application/json",
        }

        # get the file type header
        file_type_header = File.determine_mime_type(file_type)

        # set the files up for the RegScale API Call
        files = [
            (
                "file",
                (
                    file_name,
                    file_data or open(file_path, "rb").read(),
                    file_type_header,
                ),
            )
        ]

        file_like_object = BytesIO(file_data) if file_data else open(file_path, "rb")

        with file_like_object:
            data = {
                "id": parent_id,
                "module": parent_module,
                "shaHash": compute_hash(file_like_object),
            }

        # make the api call
        file_response = api.post(
            url=f"{api.config['domain']}/api/files/file",
            headers=file_headers,
            data=data,
            files=files,
        )
        if not file_response:
            api.logger.warning("File upload failed. Please check the file path and try again.")
            return None
        elif not file_response.ok:
            api.logger.warning("%s - %s", file_response.status_code, file_response.text)
            return None
        else:
            data = file_response.json()
            # Check if backend returned an error in the response body
            if data.get("status") == "error":
                error_msg = data.get("message", "Unknown error")
                api.logger.warning("File upload rejected by server: %s", error_msg)
                return {"error": error_msg}
            data["size"] = file_size
            return data

    @staticmethod
    def determine_mime_type(file_type: str) -> Optional[str]:
        """
        Function to determine the mime type of a file

        :param str file_type: The file type
        :return: The mime type, if able to determine
        :rtype: Optional[str]
        """
        log = logging.getLogger("regscale")

        # Check for missing or empty extension
        if not file_type or file_type == ".":
            log.warning("File has no extension. RegScale requires files to have extensions for upload.")
            return None

        # see file_type is an acceptable format and set the file_type_header accordingly
        try:
            file_type_header = mimetypes.types_map[file_type]
        except KeyError:
            if file_type == ".xlsx":
                file_type_header = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif file_type == ".docx":
                file_type_header = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif file_type == ".pptx":
                file_type_header = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            elif file_type == ".nessus":
                file_type_header = "text/xml"
            elif file_type == ".gz":
                file_type_header = "application/gzip"
            elif file_type == ".msg":
                file_type_header = "application/vnd.ms-outlook"
            elif file_type == ".jsonl":
                file_type_header = "application/jsonl+json"
            else:
                log.warning("Unacceptable file type for upload: %s", file_type)
                return None
        return file_type_header

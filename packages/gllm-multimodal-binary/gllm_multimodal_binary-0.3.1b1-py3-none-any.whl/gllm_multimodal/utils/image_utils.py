"""Utility functions for image-to-text operations in Gen AI applications.

This module provides a comprehensive set of utility functions for handling image data
in various formats and sources. It includes functionality for:
1. Image validation and format checking
2. Image loading from various sources (file, URL, base64, S3)
3. Image format conversion and encoding

Authors:
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    NONE
"""

import base64
import os
import re
from typing import Any
from urllib.parse import urlparse

import magic
import requests
from gllm_core.utils.logger_manager import LoggerManager

from gllm_multimodal.constants import ImageToTextConstants
from gllm_multimodal.utils.gdrive_utils import get_file_from_gdrive
from gllm_multimodal.utils.s3_utils import get_file_from_s3
from gllm_multimodal.utils.source_utils import get_file_from_file_path, get_file_from_url

logger = LoggerManager().get_logger(__name__)


def is_binary_image(image_binary_data: bytes) -> bool:
    """Validate if the provided binary data represents a valid image file.

    This function attempts to open the binary data as an image using PIL (Python Imaging Library)
    to verify if it represents a valid image format.

    Args:
        image_binary_data (bytes): The binary data to validate.

    Returns:
        bool: True if the binary data represents a valid image that can be opened by PIL,
            False otherwise.
    """
    try:
        magic_instance = magic.Magic(mime=True)
        mime_type = magic_instance.from_buffer(image_binary_data)
        if not mime_type.startswith("image/"):
            raise ValueError(f"Not an image file. Detected MIME type: {mime_type}")
        return True
    except Exception as e:
        logger.debug("The provided binary data is not a valid image file with error: %s", e)
        return False


def get_image_from_base64(image_source: str) -> bytes | None:
    """Decode and validate a base64 encoded image string.

    This function attempts to:
    1. Decode the provided base64 string
    2. Validate that the decoded data represents a valid image
    3. Return the binary data if both steps succeed

    Args:
        image_source (str): The base64 encoded image string to decode.
            Should be a valid base64 string without the data URI prefix
            (e.g., without 'data:image/jpeg;base64,').

    Returns:
        bytes | None: The decoded image binary data if successful and valid,
            None if either the decoding fails or the data is not a valid image.

    Note:
        1. The function performs validation using is_binary_image()
        2. Invalid base64 strings or non-image data will return None
        3. Logs debug messages on failure for troubleshooting
    """
    try:
        logger.debug("Attempting to decode base64 encoded image string")
        binary_data = base64.b64decode(image_source, validate=True)
        return binary_data if is_binary_image(binary_data) else None
    except Exception as e:
        logger.debug("The provided image source is not a valid base64 encoded image string with error: %s", e)
        return None


# TODO: Add support retry when failed if needed
async def get_image_binary(image_source: Any) -> tuple[bytes | None, str | None]:
    """Retrieve image binary data from various sources.

    This function acts as a unified interface for retrieving image data from different sources:
    1. Local file paths
    2. URLs (HTTP/HTTPS)
    3. Base64 encoded strings
    4. S3 URLs (s3:// or https://)

    The function automatically detects the source type and uses the appropriate method
    to retrieve the image data.

    Args:
        image_source (Any): The source of the image, which can be:
            1. bytes: Direct binary data
            2. str: Base64 string, file path, URL, or S3 URL

    Returns:
        tuple[bytes | None, str | None]: A tuple containing:
            1. The image binary data if successful, None if failed
            2. The filename if available, None for direct binary or base64
    """
    char_limit_for_debug = 512
    if isinstance(image_source, str) and len(image_source) > char_limit_for_debug:
        logger.debug("Getting image binary data from source: %s", image_source[:char_limit_for_debug])
    else:
        logger.debug("Getting image binary data from source: %s", image_source)

    if result := _get_image_from_binary_or_base64(image_source):
        return result

    if result := await _get_image_from_external_source(image_source):
        return result

    logger.debug("Failed to get image binary data from source: %s", image_source)
    raise ValueError("Unsupported image format")


def _get_image_from_binary_or_base64(image_source: Any) -> tuple[bytes | None, str | None] | None:
    """Handle binary data or base64 encoded image sources.

    Args:
        image_source (Any): The image source to check

    Returns:
        tuple[bytes | None, str | None] | None: Image binary and filename if successful, None if not applicable
    """
    if isinstance(image_source, bytes) and is_binary_image(image_source):
        logger.debug("Image source is valid binary data")
        return image_source, ImageToTextConstants.NOT_GIVEN

    if image_binary := get_image_from_base64(image_source):
        if is_binary_image(image_binary):
            logger.debug("Image source is a valid base64 encoded image string")
            return image_binary, ImageToTextConstants.NOT_GIVEN

    return None


async def _get_image_from_external_source(image_source: Any) -> tuple[bytes | None, str | None] | None:
    """Handle URLs, file paths and S3 image sources.

    Args:
        image_source (Any): The image source to check

    Returns:
        tuple[bytes | None, str | None] | None: Image binary and filename if successful, None if not applicable
    """
    if image_binary := get_file_from_file_path(image_source):
        if is_binary_image(image_binary):
            logger.debug("Image source is a valid image file path: %s", image_source)
            return image_binary, os.path.basename(image_source)

    if image_binary := await get_file_from_url(image_source):
        if is_binary_image(image_binary):
            logger.debug("Image source is a valid image URL: %s", image_source)
            parsed = urlparse(image_source)
            return image_binary, os.path.basename(parsed.path)

    if image_binary := get_file_from_s3(image_source):
        if is_binary_image(image_binary):
            logger.debug("Image source is a valid S3 URL: %s", image_source)
            parsed = urlparse(image_source)
            key = parsed.path.lstrip("/")
            return image_binary, os.path.basename(key)

    if image_binary := get_file_from_gdrive(image_source):
        if is_binary_image(image_binary):
            logger.debug("Image source is a valid Google Drive URL: %s", image_source)
            parsed = urlparse(image_source)
            return image_binary, os.path.basename(parsed.path)

    return None


def get_unique_non_empty_strings(texts: list[str]) -> list[str]:
    """Get unique non-empty strings from a list of strings and remove whitespace.

    This function takes a list of strings and returns a list of strings where each
    string from the list is not empty or whitespace-only. It also removes duplicates.

    Args:
        texts (list[str]): A list of strings to combine.

    Returns:
        list[str]: A list of strings where each string is not empty or whitespace-only.
    """
    return [] if not texts else list(dict.fromkeys(text.strip() for text in texts if text.strip()))


def combine_strings(texts: list[str]) -> str:
    """Combine multiple strings into a single string with newline separators.

    This function takes a list of strings and returns a single string where each
    string from the list is on a new line. It filters out any empty or whitespace-only
    strings from the list before joining them.

    Args:
        texts (list[str]): A list of strings to combine.

    Returns:
        str: A single string containing all valid strings, where each string is on a new line.
    """
    return "\n".join(text for text in texts) if texts else ""

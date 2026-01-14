"""Utility functions for downloading files from various sources.

Authors:
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    None
"""

import base64
import http

from aiohttp import ClientSession
from gllm_core.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


async def get_file_from_url(file_source: str, timeout: int = 30, session: ClientSession | None = None) -> bytes | None:
    """Asynchronously download and validate an image from a URL.

    This function performs the following steps:
    1. Attempts to download the content from the provided URL.
    2. Validates that the downloaded content is a valid image.
    3. Returns the binary data if both steps succeed.

    Args:
        file_source (str): The URL of the file to download.
            Supports HTTP and HTTPS protocols.
        timeout (int, optional): The timeout for the HTTP request in seconds.
            Defaults to 30 seconds.
        session (Optional[aiohttp.ClientSession], optional): An existing aiohttp session to use.
            If None, a new session will be created. Defaults to None.

    Returns:
        bytes | None: The downloaded image binary data if successful and valid,
            None if the download fails or the content is not a valid image.
    """
    try:
        logger.debug("Attempting to download file from URL: %s", file_source)
        should_close_session = session is None
        session = session or ClientSession()

        try:
            async with session.get(file_source, timeout=timeout) as response:
                if response.status == http.HTTPStatus.OK:
                    content = await response.read()
                    return content
                logger.debug("Failed to download file with response status code: %s", response.status)
                return None
        finally:
            if should_close_session:
                await session.close()
    except Exception as e:
        logger.debug("The provided image source is not a valid URL with error: %s", e)
        return None


def get_file_from_file_path(source: str) -> bytes | None:
    """Read image file and return its binary data if valid.

    Args:
        source (str): Path to the image file.

    Returns:
        bytes | None: Binary data of the image file if valid, None otherwise.
    """
    try:
        logger.debug("Attempting to read image file from file path: %s", source)
        with open(source, "rb") as file:
            image_data = file.read()
            return image_data
    except Exception as e:
        logger.debug("The provided image source is not a valid image file path with error: %s", e)
        return None


def encode_file_to_base64(file_binary: bytes) -> str:
    """Convert binary file data to base64 string.

    Args:
        file_binary (bytes): Binary data of the file.

    Returns:
        str: Base64 encoded string.
    """
    return base64.b64encode(file_binary).decode("utf-8")

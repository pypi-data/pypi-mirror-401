"""Module for downloading images from S3 URLs.

This module provides a class for downloading file from S3 URLs.

It will first try to connect using default credentials (instance profile, environment variables, etc),
and if that fails, it will explicitly check for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment
variables. If those fail, it will check for AWS_SESSION_TOKEN.

Authors:
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    None
"""

import os
from typing import Any
from urllib.parse import urlparse

from gllm_core.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


def get_file_from_s3(url: str) -> bytes | None:
    """Get file from S3 bucket.

    This function attempts to get a file from an S3 bucket using:
    1. Default credentials (from AWS CLI or instance profile).
    2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
    3. Session token if available.

    Args:
        url (str): The S3 URL to get the file from.
            Can be in the format:
            1. s3://bucket/key.
            2. https://bucket.s3.amazonaws.com/key.

    Returns:
        bytes | None: The file contents if successful, None otherwise

    Raises:
        ValueError: If AWS credentials are not found or invalid.
    """
    if not url:
        return None

    try:
        bucket_name, key = _parse_s3_url(url)
        if not bucket_name or not key:
            logger.debug("Invalid S3 URL format: %s", url)
            return None

        return _try_download_with_credentials(bucket_name, key)

    except Exception as e:
        logger.error("Failed to get file from S3: %s", e)
        return None


def _parse_s3_url(s3_uri: str) -> tuple[str | None, str | None]:
    """Parse S3 URL into bucket name and key.

    Args:
        s3_uri (str): The S3 URL to parse.

    Returns:
        tuple[str | None, str | None]: Tuple of (bucket_name, key) or (None, None) if invalid.
    """
    parsed = urlparse(s3_uri)
    if s3_uri.startswith("s3://"):
        return parsed.netloc, parsed.path.lstrip("/")

    if not parsed.netloc.endswith(".amazonaws.com"):
        logger.debug("Not a valid S3 URL: %s", s3_uri)
        return None, None
    host_parts = parsed.netloc.split(".")

    return host_parts[0], parsed.path.lstrip("/")


def _try_download_with_credentials(bucket_name: str, key: str) -> bytes | None:
    """Try downloading with different credential configurations.

    Args:
        bucket_name (str): S3 bucket name.
        key (str): S3 object key.

    Returns:
        bytes | None: File data if successful, None otherwise.

    Raises:
        ValueError: If no valid credentials are found.
    """
    import boto3

    try:
        return _download_from_s3(boto3.client("s3"), bucket_name, key)
    except Exception:
        logger.debug("Failed to connect with default credentials")

    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")

    if access_key and secret_key:
        try:
            s3_client = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            return _download_from_s3(s3_client, bucket_name, key)
        except Exception:
            logger.debug("Failed to connect with access key and secret key")

            if session_token:
                try:
                    s3_client = boto3.client(
                        "s3",
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        aws_session_token=session_token,
                    )
                    return _download_from_s3(s3_client, bucket_name, key)
                except Exception:
                    logger.debug("Failed to connect with session token")

    raise ValueError(
        "AWS credentials not found or invalid. Please ensure valid credentials are available "
        "through environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) "
        "or default credential providers."
    ) from None


def _download_from_s3(s3_client: Any, bucket_name: str, key: str) -> bytes | None:
    """Download and validate image from S3.

    Args:
        s3_client: Boto3 S3 client.
        bucket_name (str): S3 bucket name.
        key (str): S3 object key.

    Returns:
        bytes | None: File data if valid, None otherwise.
    """
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    image_data = response["Body"].read()
    return image_data

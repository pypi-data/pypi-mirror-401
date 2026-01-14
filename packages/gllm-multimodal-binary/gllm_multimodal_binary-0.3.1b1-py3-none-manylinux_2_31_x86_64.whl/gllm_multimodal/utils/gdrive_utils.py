"""Module for downloading files from Google Drive.

Authors:
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    NONE
"""

import os
import re
from io import BytesIO

import requests
from gllm_core.utils.logger_manager import LoggerManager
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

logger = LoggerManager().get_logger(__name__)


def get_file_from_gdrive(gdrive_source: str) -> bytes | None:
    """Download a file from Google Drive given a file ID or URL.

    Args:
        gdrive_source (str): Google Drive file ID or full URL.

    Returns:
        bytes | None: The file's binary content if successful, None otherwise.
    """
    file_id = _extract_gdrive_file_id(gdrive_source)
    if not file_id:
        return None

    if content := _download_gdrive_direct(file_id):
        return content
    return _download_gdrive_api(file_id)


def _extract_gdrive_file_id(gdrive_source: str) -> str | None:
    """Extract file ID from a Google Drive URL or direct ID.

    Args:
        gdrive_source (str): Google Drive file ID or full URL.

    Returns:
        str | None: Extracted file ID if successful, None otherwise.
    """
    patterns = {
        r"https?://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)": 1,
        r"https?://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)": 1,
        r"https?://drive\.google\.com/uc\?id=([a-zA-Z0-9_-]+)": 1,
        r"^([a-zA-Z0-9_-]{20,})$": 1,  # direct file ID
    }

    file_id = next(
        (re.search(pattern, gdrive_source).group(1) for pattern in patterns if re.search(pattern, gdrive_source)), None
    )

    if not file_id:
        logger.debug("Could not extract Google Drive file ID from source: %s", gdrive_source)

    return file_id


def _download_gdrive_direct(file_id: str) -> bytes | None:
    """Attempt direct download from Google Drive without API.

    Args:
        file_id (str): Google Drive file ID.

    Returns:
        bytes | None: File content if successful, None otherwise.
    """
    try:
        with requests.Session() as session:
            response = session.get(
                "https://drive.google.com/uc", params={"export": "download", "id": file_id}, stream=True
            )

            if token := next(
                (value for key, value in response.cookies.items() if key.startswith("download_warning")), None
            ):
                response = session.get(
                    "https://drive.google.com/uc",
                    params={"export": "download", "id": file_id, "confirm": token},
                    stream=True,
                )
            response.raise_for_status()
            content = response.content
            try:
                snippet = content.decode("utf-8", errors="ignore")
                if (
                    "Sign in" in snippet
                    or "To access this item, you need to sign in" in snippet
                    or "accounts.google.com/ServiceLogin" in snippet
                    or "gaia_loginform" in snippet
                ):
                    logger.debug("Google Drive direct download response indicates sign-in required.")
                    return None
            except Exception as e:
                logger.debug("Error decoding Google Drive response for sign-in check: %s", e)
            return content

    except Exception as e:
        logger.debug("Failed direct download from Google Drive: %s", e)
        return None


def _download_gdrive_api(file_id: str) -> bytes | None:
    """Download from Google Drive using API with service account credentials.

    Args:
        file_id (str): Google Drive file ID.

    Returns:
        bytes | None: File content if successful, None otherwise.
    """
    gcp_credentials_path = os.environ.get("GCP_CREDENTIALS") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not gcp_credentials_path or not os.path.exists(gcp_credentials_path):
        logger.debug("No GCP credentials found for Google Drive API download")
        return None

    try:
        creds = service_account.Credentials.from_service_account_file(
            gcp_credentials_path, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )

        with build("drive", "v3", credentials=creds) as service:
            request = service.files().get_media(fileId=file_id)
            fh = BytesIO()
            downloader = MediaIoBaseDownload(fh, request)

            while not downloader.next_chunk()[1]:
                pass

            return fh.getvalue()

    except Exception as e:
        logger.debug("Failed to download from Google Drive using API: %s", e)
        return None

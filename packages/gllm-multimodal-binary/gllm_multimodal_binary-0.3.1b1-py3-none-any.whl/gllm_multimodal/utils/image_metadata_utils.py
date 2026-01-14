"""Utility functions for image metadata extraction.

Authors:
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    NONE
"""

import logging
from io import BytesIO
from typing import Any

import exifread
from gllm_core.utils.logger_manager import LoggerManager

from gllm_multimodal.constants import ExifConstants

logger = LoggerManager().get_logger()

semantic_router_logger = logging.getLogger("exifread")
semantic_router_logger.handlers = logger.handlers
semantic_router_logger.setLevel(logger.level)
semantic_router_logger.propagate = logger.propagate


def get_image_metadata(image_binary: bytes) -> dict[str, Any]:
    """Extract metadata from image binary data.

    This function extracts metadata from the image, including:
    1. GPS coordinates (latitude/longitude) if available in EXIF data

    Args:
        image_binary (bytes): The binary data of the image.

    Returns:
        dict[str, Any]: Dictionary containing image metadata.
    """
    metadata = {}

    image_file = BytesIO(image_binary)
    tags = exifread.process_file(image_file, details=False)

    lat_val = _extract_gps_coordinate(tags, ExifConstants.GPS_LATITUDE, ExifConstants.GPS_LATITUDE_REF)
    if lat_val is not None:
        metadata[ExifConstants.LATITUDE] = lat_val

    lon_val = _extract_gps_coordinate(tags, ExifConstants.GPS_LONGITUDE, ExifConstants.GPS_LONGITUDE_REF)
    if lon_val is not None:
        metadata[ExifConstants.LONGITUDE] = lon_val

    return metadata


def _extract_gps_coordinate(tags: dict, coordinate_tag: str, reference_tag: str) -> float | None:
    """Extract GPS coordinate from EXIF tags.

    Args:
        tags (dict): EXIF tags dictionary from exifread.
        coordinate_tag (str): Tag name for coordinate values (e.g., "GPS GPSLatitude").
        reference_tag (str): Tag name for coordinate reference (e.g., "GPS GPSLatitudeRef").

    Returns:
        float | None: GPS coordinate in decimal degrees, or None if not available.
    """
    if coordinate_tag in tags and reference_tag in tags:
        coordinate_values = tags[coordinate_tag].values
        coordinate_ref = str(tags[reference_tag])
        coordinate_val = _convert_gps_coordinates_exifread(coordinate_values)
        if coordinate_ref in {ExifConstants.GPS_WEST, ExifConstants.GPS_SOUTH}:
            coordinate_val = -coordinate_val
        return coordinate_val
    return None


def _convert_gps_coordinates_exifread(coordinate_values: list[int]) -> float:
    """Convert GPS coordinates from ExifRead format to decimal degrees.

    ExifRead returns GPS coordinates as a list of Ratio objects.

    Args:
        coordinate_values (list[int]): List of coordinate values from ExifRead.

    Returns:
        float: The GPS coordinates in decimal degrees.
    """
    degrees = float(coordinate_values[0])
    minutes = float(coordinate_values[1]) / 60
    seconds = float(coordinate_values[2]) / 3600
    return degrees + minutes + seconds

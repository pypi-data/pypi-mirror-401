"""Constants for image-to-text operations in Gen AI applications.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    NONE
"""

from enum import StrEnum


class ImageToTextConstants:
    """Constants for image-to-text operations in Gen AI applications."""

    NOT_GIVEN = "not_given"
    FILENAME = "filename"
    NO_IMAGE_FILENAME = "no_image_filename"


class CaptionConstants:
    """Constants for caption operations in Gen AI applications."""

    CAPTION_DEFAULT_JSON_KEY = "captions"
    DOMAIN_KNOWLEDGE = "domain_knowledge"
    IMAGE_DESCRIPTION = "image_description"
    IMAGE_METADATA = "image_metadata"
    IMAGE_ONE_LINER = "image_one_liner"
    NUMBER_OF_CAPTIONS = "number_of_captions"
    ATTACHMENTS_CONTEXT = "attachments_context"

    DEFAULT_NUMBER_OF_CAPTIONS = 5


class ExifConstants:
    """Constants for EXIF tag operations in image metadata extraction."""

    GPS_LATITUDE = "GPS GPSLatitude"
    GPS_LATITUDE_REF = "GPS GPSLatitudeRef"
    GPS_LONGITUDE = "GPS GPSLongitude"
    GPS_LONGITUDE_REF = "GPS GPSLongitudeRef"

    GPS_SOUTH = "S"
    GPS_WEST = "W"

    LATITUDE = "latitude"
    LONGITUDE = "longitude"


class Modality(StrEnum):
    """Defines supported modalities."""

    IMAGE = "image"
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"


class ModalityConverterApproach(StrEnum):
    """Defines supported modality converter approach types."""

    LM_BASED = "lm_based"
    WHISPER = "whisper"
    GEMINI = "gemini"
    GOOGLE_CLOUD = "google_cloud"
    PROSA = "prosa"
    YOUTUBE = "youtube"


class ModalityConverterTask(StrEnum):
    """Defines supported modality converter tasks."""

    CAPTIONING = "captioning"
    MERMAID = "mermaid"
    TRANSCRIPT = "transcript"
    AUTO = "auto"

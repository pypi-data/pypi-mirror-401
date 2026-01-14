"""Schema for image captioning operations in Gen AI applications.

This module defines the data structures for representing results from
image captioning operations. It provides:
1. Result class for image captions
2. Support for multiple caption types
3. Metadata storage
4. Domain knowledge integration
5. External context support through attachments

Authors:
    Yanfa Adi Putra (yanfa.a.putra@gdplabs.id)
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from gllm_inference.schema import Attachment
from pydantic import BaseModel, Field, field_validator

from gllm_multimodal.constants import (
    CaptionConstants,
    ImageToTextConstants,
)
from gllm_multimodal.utils.image_utils import get_image_binary


class Caption(BaseModel):
    """Result class for image captioning operations.

    This class extends ImageToTextResult to provide a structured format
    for image captioning results, supporting:
    - Multiple caption types (one-liner, detailed, domain-specific)
    - Caption count tracking
    - Metadata storage for processing details

    Attributes:
        image_one_liner (str): Brief, single-sentence summary of the image.
            Defaults to empty string if not provided.
        image_description (str): Detailed, multi-sentence description of the image.
            Defaults to empty string if not provided.
        domain_knowledge (str): Domain-specific interpretation or context.
            Defaults to empty string if not provided.
        number_of_captions (int): Total number of distinct captions generated.
            Defaults to 0 if no captions are generated.
        image_metadata (dict[str, Any]): Additional information about the image such as image location.
        attachments_context (list[Attachment]): Optional list of external context
            objects (files, bytes, or pre-processed inputs) that can enrich
            captioning results. Bytes are automatically converted into Attachment
            objects via `Attachment.from_bytes`.

    Example:
        >>> Caption(
        ...     image_one_liner="A cat sitting on a couch",
        ...     image_description="A fluffy orange cat resting on a blue sofa in a living room.",
        ...     attachments_context=[
        ...         b"raw image bytes here",
        ...         Attachment.from_bytes(b'some bytes', filename="context.png"),
        ...     ]
        ... )
    """

    image_one_liner: str = Field(default=ImageToTextConstants.NOT_GIVEN)
    image_description: str = Field(default=ImageToTextConstants.NOT_GIVEN)
    domain_knowledge: str = Field(default=ImageToTextConstants.NOT_GIVEN)
    number_of_captions: int = Field(default=CaptionConstants.DEFAULT_NUMBER_OF_CAPTIONS)
    language: str = Field(default="Indonesian")
    image_metadata: dict[str, Any] = Field(default={})
    attachments_context: list[Attachment] = Field(default=[])

    @field_validator("image_one_liner", "image_description", "domain_knowledge", "language", mode="before")
    def handle_none_values(str_value: Any) -> Any:
        """Handle None values by converting them to default values."""
        if str_value is None:
            return ImageToTextConstants.NOT_GIVEN
        return str_value

    @field_validator("number_of_captions", mode="before")
    def handle_none_number_of_captions(caption_value: Any) -> Any:
        """Handle None values for number_of_captions by using default."""
        if caption_value is None:
            return CaptionConstants.DEFAULT_NUMBER_OF_CAPTIONS
        return caption_value

    @field_validator("image_metadata", mode="before")
    def handle_none_metadata(metadata_value: Any) -> Any:
        """Handle None values for image_metadata by using empty dict."""
        if metadata_value is None:
            return {}
        return metadata_value

    @field_validator("attachments_context", mode="before")
    def handle_none_attachments(cls, attachments_value: Any) -> Any:
        """Normalize and validate `attachments_context`.

        This method ensures that the `attachments_context` field is always a list of
        `Attachment` objects. It handles multiple input cases:

        - None → returns an empty list
        - list[bytes] → converts each item into an Attachment via `Attachment.from_bytes`
        - list[Attachment] → keeps as-is
        - list[mixed] → normalizes supported types, raises error on unsupported types
        - any other type → raises TypeError

        Args:
            attachments_value (Any): Input value provided to `attachments_context`.

        Returns:
            list[Attachment]: A normalized list of `Attachment` objects.

        Raises:
            TypeError: If an unsupported type is provided (e.g., str, dict).
        """
        if attachments_value is None:
            return []

        if isinstance(attachments_value, list):
            normalized = []
            for item in attachments_value:
                if isinstance(item, Attachment):
                    normalized.append(item)
                elif isinstance(item, bytes):
                    normalized.append(Attachment.from_bytes(item))
                else:
                    try:
                        asyncio.get_running_loop()
                        with ThreadPoolExecutor() as executor:
                            future = executor.submit(asyncio.run, get_image_binary(item))
                            image_bin, filename = future.result()
                    except RuntimeError:
                        image_bin, filename = asyncio.run(get_image_binary(item))

                    normalized.append(Attachment.from_bytes(image_bin, filename=filename))

            return normalized

        raise TypeError(f"Unsupported attachments_context type: {type(attachments_value)}")

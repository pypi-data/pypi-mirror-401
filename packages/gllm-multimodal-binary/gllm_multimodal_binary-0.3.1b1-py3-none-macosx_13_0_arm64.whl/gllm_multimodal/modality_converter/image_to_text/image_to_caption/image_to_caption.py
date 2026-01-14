"""Base class for image captioning implementations in Gen AI applications.

This module provides the foundation for converting images to natural language captions.
It supports various types of captioning:
1. One-line summaries
2. Detailed descriptions
3. Domain-specific interpretations
4. Multiple caption generation

Authors:
    Yanfa Adi Putra (yanfa.a.putra@gdplabs.id)

References:
    NONE
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_multimodal.modality_converter.image_to_text.image_to_text import BaseImageToText
from gllm_multimodal.modality_converter.schema.caption import Caption
from gllm_multimodal.modality_converter.schema.text_result import TextResult
from gllm_multimodal.utils.image_metadata_utils import get_image_metadata
from gllm_multimodal.utils.image_utils import (
    combine_strings,
    get_unique_non_empty_strings,
)


class BaseImageToCaption(BaseImageToText, ABC):
    """Abstract base class for image captioning operations in Gen AI applications.

    This class extends ImageToText to provide specialized functionality for generating
    captions from images. It supports multiple captioning styles and can incorporate additional context
    like oneliner of image, description of image, domain knowledge and metadata.
    """

    async def _convert(
        self,
        image_binary: bytes,
        filename: str,
        **kwargs: Any,
    ) -> TextResult:
        """Convert an image to natural language captions with optional context.

        This method orchestrates the complete image captioning process:
        1. Loads and validates the image from the source
        2. Extracts image metadata (focus on GPS from EXIF data)
        3. Generates captions
        4. Combines the results

        Args:
            image_binary (bytes): The binary data of the image.
            filename (str): The filename of the image.
            **kwargs (Any): Additional keyword arguments including:
                1. number_of_captions (int, optional): Number of captions to generate (default: 5).
                2. image_oneliner (str, optional): Brief one-line summary or title (default: "Not given").
                3. image_description (str, optional): Detailed description of the image (default: "Not given").
                4. domain_knowledge (str, optional): Relevant domain-specific information (default: "Not given").
                5. attachments_context (list[bytes | Attachment], optional): A list of attachment formated
                    as Attachment or bytes.
                6. use_metadata (bool, optional): Whether to use image metadata (default: True).

        Returns:
            TextResult: A structured result containing:
                1. text: Combined captions as a single string.
                2. metadata: A CaptionResult object containing:
                   1. one_liner: Brief one-line summary of the image.
                   2. description: Detailed multi-sentence description.
                   3. domain_knowledge: Domain-specific context and interpretation.
                   4. number_of_captions: Total number of captions generated.
                   5. image_metadata: Extracted EXIF and other image metadata.
                   6. attachments_context: additional attachments for caption enricher.

        Raises:
            ValueError: If the image source is invalid or inaccessible
            RuntimeError: If caption generation fails
        """
        use_metadata = kwargs.get("use_metadata", True)
        delete_attachments_context = kwargs.get("delete_attachments_context", True)
        metadata = get_image_metadata(image_binary) if use_metadata else {}

        caption_data = Caption(
            image_metadata=metadata,
            **kwargs,
        )

        captions = await self._get_captions(
            image_binary=image_binary,
            filename=filename,
            caption_data=caption_data,
            **kwargs,
        )
        cleaned_captions = get_unique_non_empty_strings(captions)
        caption_data.number_of_captions = len(cleaned_captions)

        if delete_attachments_context:
            caption_data.attachments_context = []

        return TextResult(result=combine_strings(cleaned_captions), tag="caption", metadata=caption_data)

    @abstractmethod
    async def _get_captions(
        self,
        image_binary: bytes,
        filename: str,
        caption_data: Caption,
        **kwargs: Any,
    ) -> list[str]:
        """Generate captions for an image using provided context and configuration.

        This abstract method must be implemented by subclasses to define the specific
        caption generation logic. The implementation should consider all provided context
        and adhere to the specified captioning standards.

        Args:
            image_binary (bytes): The raw binary data of the image to caption.
            filename (str): Name of the image file, used for reference.
            caption_data (Caption): Caption data containing:
                1. image_oneliner (str): Brief one-line summary or title (default: "Not given").
                2. image_description (str): Detailed description of the image (default: "Not given").
                3. domain_knowledge (str): Relevant domain-specific information (default: "Not given").
                4. image_metadata (dict[str, Any]): Image metadata EXIF for data GPS coordinates if available.
                5. number_of_captions (int, optional): Number of captions to generate (default: 5).
            **kwargs (Any): Additional keyword arguments.

        Returns:
            list[str]: A list of generated captions.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
            ValueError: If the image data is invalid or cannot be processed.
        """
        raise NotImplementedError

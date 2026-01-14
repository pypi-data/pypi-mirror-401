"""Base class for image to mermaid implementations in Gen AI applications.

This module provides the foundation for converting images to mermaid syntax.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_multimodal.modality_converter.image_to_text.image_to_text import BaseImageToText
from gllm_multimodal.modality_converter.schema.mermaid import Mermaid
from gllm_multimodal.modality_converter.schema.text_result import TextResult


class BaseImageToMermaid(BaseImageToText, ABC):
    """Abstract base class for image-to-mermaid converters.

    This class provides a standardized `_convert` implementation and defines
    the interface `_get_mermaid`, which must be implemented by subclasses.

    Subclasses should implement logic to process an image and produce a
    Mermaid syntax string that represents the structure of the diagram.
    """

    async def _convert(self, image_binary: bytes, **kwargs) -> TextResult:
        """Converts an image to Mermaid syntax and wraps it in a TextResult.

        Args:
            image_binary (bytes): The binary content of the image.
            filename (str): The name of the image file.
            **kwargs: Additional parameters used to construct Mermaid metadata.

        Returns:
            TextResult: A container holding the Mermaid syntax and associated metadata.
        """
        mermaid_metadata = Mermaid(**kwargs)
        mermaid_syntax = await self._get_mermaid(image_binary, mermaid_metadata, **kwargs)
        return TextResult(result=mermaid_syntax or "", tag="mermaid", metadata=mermaid_metadata)

    @abstractmethod
    async def _get_mermaid(self, image_binary: bytes, mermaid_data: Mermaid, **kwargs: Any) -> str:
        """Abstract method to extract Mermaid syntax from an image.

        Must be implemented by subclasses to define how image-to-mermaid
        conversion is performed.

        Args:
            image_binary (bytes): The binary content of the image.
            mermaid_data (Mermaid): Pre-validated Mermaid metadata or parameters.
            **kwargs (Any): Additional context or control parameters.

        Returns:
            str: A string containing valid Mermaid diagram syntax.

        Raises:
            NotImplementedError: If the subclass does not override this method.
        """
        raise NotImplementedError

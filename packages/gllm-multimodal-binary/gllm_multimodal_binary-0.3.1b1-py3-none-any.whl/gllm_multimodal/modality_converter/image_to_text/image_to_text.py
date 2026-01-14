"""Defines a base class for image to text converter used in Gen AI applications.

This module provides the foundation for converting images to text in various formats,
including OCR, image captioning, and other image analysis tasks.

Authors:
    Yanfa Adi Putra (yanfa.a.putra@gdplabs.id)

References:
    NONE
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_core.utils.logger_manager import LoggerManager

from gllm_multimodal.modality_converter.modality_converter import BaseModalityConverter
from gllm_multimodal.modality_converter.schema.text_result import TextResult
from gllm_multimodal.utils.image_utils import get_image_binary


class BaseImageToText(BaseModalityConverter, ABC):
    """An abstract base class for image to text conversion used in Gen AI applications.

    This class provides a foundation for building image to text converter components in Gen AI applications.
    It supports various types of image sources (file paths, URLs, base64 strings) and can be extended
    to implement different types of image analysis tasks like OCR, captioning, or object detection.
    """

    def __init__(self):
        """Initialize the base image to text component with logging capabilities."""
        self._logger = LoggerManager().get_logger(self.__class__.__name__)

    async def convert(self, source: str | bytes, **kwargs: Any) -> TextResult:
        """Executes the image to text process.

        This method validates the input parameters and calls `convert` to perform the image to text process.
        It ensures that the required image_source parameter is provided and valid before proceeding.

        Args:
            source (str | bytes): The source of the image to convert to text.
            **kwargs (Any): A dictionary of arguments required for the image to text process.
                Must include `source` of type `str`.
                May include additional parameters specific to the implementation.

        Returns:
            ImageToTextResult: The result of processing the image.

        Raises:
            ValueError: If `source` is missing from the input kwargs or is empty.
            TypeError: If `source` is not a string or bytes.
        """
        if not isinstance(source, (str, bytes)):
            raise TypeError("The `source` must be of type `str` or `bytes`.")

        if isinstance(source, str) and not source.strip():
            raise ValueError("The `source` cannot be an empty string.")

        try:
            image_binary, filename = await get_image_binary(source)
        except ValueError as e:
            self._logger.error(f"Error getting image binary: {e}")
            return TextResult(result="", tag="")

        return await self._convert(image_binary, filename=filename, **kwargs)

    @abstractmethod
    async def _convert(self, image_binary: bytes, filename: str, **kwargs) -> TextResult:
        """Process the image and convert it to text.

        This abstract method must be implemented by subclasses to define how the image is converted to text.
        It supports various image sources and can be customized for different types of text extraction tasks.

        Args:
            image_binary (bytes): The binary data of the image.
            filename (str): The filename of the image.
            **kwargs: Additional configuration parameters specific to each implementation.
                These parameters allow customization of the conversion process.

        Returns:
            ImageToTextResult: The result of processing the image, containing:
                1. Extracted text or generated captions.
                2. Metadata about the image.
                3. Additional processing information.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

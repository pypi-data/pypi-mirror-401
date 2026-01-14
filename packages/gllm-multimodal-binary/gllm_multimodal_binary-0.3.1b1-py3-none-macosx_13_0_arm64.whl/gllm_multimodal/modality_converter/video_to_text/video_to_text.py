"""Defines a base class for video-to-text converters used in Gen AI applications.

This module provides an abstract base class `BaseVideoToText` which defines a
common interface for converting video content into text. It handles initial
input validation and delegates the actual conversion process to a subclass
implementation via the `_convert` method.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_inference.schema import Attachment

from gllm_multimodal.modality_converter.modality_converter import BaseModalityConverter
from gllm_multimodal.modality_converter.schema.text_result import TextResult


class BaseVideoToText(BaseModalityConverter, ABC):
    """Abstract base class for video-to-text conversion."""

    async def convert(self, source: str | bytes, **kwargs: Any) -> TextResult:
        """Executes the video to text process.

        This method validates the input parameters and calls `_convert` to perform the video to text process.
        It ensures that the required source parameter is provided and valid before proceeding.

        Args:
            source (str | bytes): The source of the video to convert to text.
            **kwargs (Any): A dictionary of arguments required for the video to text process.
                Must include `source` of type `str`.
                May include additional parameters specific to the implementation.

        Returns:
            TextResult: The result of processing the video.

        Raises:
            ValueError: If `source` is missing from the input kwargs or is empty.
            TypeError: If `source` is not a string or bytes.
        """
        if not isinstance(source, (str, bytes)):
            raise TypeError("The `source` must be of type `str` or `bytes`.")

        if not source or (isinstance(source, str) and not source.strip()):
            raise ValueError("The `source` cannot be empty.")

        if isinstance(source, bytes):
            source = Attachment.from_bytes(source)

        return await self._convert(source, **kwargs)

    @abstractmethod
    async def _convert(self, source: str | Attachment, **kwargs) -> TextResult:
        """Process the video and convert it to text.

        This abstract method must be implemented by subclasses to define how the video is converted to text.
        It supports various video sources and can be customized for different types of text extraction tasks.

        Args:
            source (str | Attachment): The data of the video.
            **kwargs: Additional configuration parameters specific to each implementation.
                These parameters allow customization of the conversion process.

        Returns:
            TextResult: The result of processing the video.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_preset(
        cls,
        preset_name: str | None = "default",
        **kwargs: Any,
    ) -> "BaseVideoToText":
        """Initialize the video to text converter using preset model configurations.

        This abstract classmethod must be implemented by subclasses to define how to create
        an instance from a preset configuration.

        Args:
            preset_name (str | None): Name of the preset to use. Defaults to "default".
            **kwargs (Any): Additional keyword arguments to pass to the preset configuration.

        Returns:
            BaseVideoToText: Initialized video to text converter using preset model.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

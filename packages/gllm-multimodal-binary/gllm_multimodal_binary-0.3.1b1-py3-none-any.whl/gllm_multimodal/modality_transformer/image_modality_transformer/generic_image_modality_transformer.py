"""This module defines a generic modality transformer that converts images into text/bytes.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

Reference:
    None
"""

from typing import Any

from gllm_multimodal.modality_converter.modality_converter import BaseModalityConverter
from gllm_multimodal.modality_transformer.image_modality_transformer.image_modality_transformer import (
    ImageModalityTransformer,
)


class GenericImageModalityTransformer(ImageModalityTransformer):
    """A generic transformer which uses a single converter to convert images to string/bytes.

    Attributes:
        converter (BaseModalityConverter): The converter used to transform images into text or bytes.
    """

    def __init__(self, converter: BaseModalityConverter):
        """Initializes the transformer with a modality converter.

        Args:
            converter (BaseModalityConverter): An instance of a modality converter responsible
                for performing the image-to-text or image-to-bytes transformation.
        """
        super().__init__()
        self.converter = converter

    async def _transform(self, source: bytes | str, query: str | None = None, **kwargs: Any) -> str | bytes:
        """Converts an image input to output based on specified converter.

        Args:
            source (bytes | str): The image to be convert into other modality, provided as raw bytes.
            query (str | None): Input query that will be used as additional information for modality transformation.
            kwargs (Any): additional arguments for converter.

        Returns:
            str | bytes: The converted image to text describing the image.
        """
        result = await self.converter.convert(source, query=query, **kwargs)

        return result.result

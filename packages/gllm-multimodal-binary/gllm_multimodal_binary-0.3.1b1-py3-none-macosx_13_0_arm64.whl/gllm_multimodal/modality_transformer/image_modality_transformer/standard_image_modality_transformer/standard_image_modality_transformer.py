"""This module defines a standard modality transformer that converts images into text/bytes via route.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

Reference:
    NONE
"""

from typing import Any

from gllm_pipeline.router.router import BaseRouter

from gllm_multimodal.modality_converter.modality_converter import BaseModalityConverter
from gllm_multimodal.modality_converter.schema import TextResult
from gllm_multimodal.modality_transformer.image_modality_transformer.image_modality_transformer import (
    ImageModalityTransformer,
)
from gllm_multimodal.modality_transformer.image_modality_transformer.standard_image_modality_transformer.preset import (
    get_preset,
)


class StandardImageModalityTransformer(ImageModalityTransformer):
    """A standardized image modality transformer that routes and applies converter.

    This class integrates a routing mechanism to dynamically select a converter
    according to the characteristics of the image input (e.g., format, content, etc.).

    Attributes:
        router (BaseRouter): A routing component that determines the route based on the input image.
        route_mapping (dict[str, BaseModalityConverter]): A mapping of route names to their corresponding
            modality converters.
    """

    def __init__(self, router: BaseRouter, route_mapping: dict[str, BaseModalityConverter]):
        """Initialize the StandardImageModalityTransformer.

        Args:
            router (BaseRouter): The router responsible for selecting the route.
            route_mapping (dict[str, BaseModalityConverter]): Mapping from route names to modality converters.

        Raises:
            ValueError: If any expected route from the router is missing in the route_mapping.
        """
        super().__init__()
        self.router = router
        self.route_mapping = self._validate_routes(route_mapping)

    @classmethod
    def from_preset(cls, preset_name: str) -> "StandardImageModalityTransformer":
        """Create an instance using a predefined preset configuration.

        Args:
            preset_name (str): Name of the preset to use.

        Returns:
            StandardImageModalityTransformer: An instance configured with the preset.
        """
        return cls(**get_preset(preset_name))

    def _validate_routes(self, route_mapping: dict[str, BaseModalityConverter]):
        """Ensure that all valid routes required by the router are provided.

        Args:
            route_mapping (dict[str, BaseModalityConverter]): Mapping of route names to converters.

        Returns:
            dict[str, BaseModalityConverter]: The validated route mapping.

        Raises:
            ValueError: If any route expected by the router is not provided in the mapping.
        """
        remaining_routes = self.router.valid_routes - set(route_mapping.keys())
        if len(remaining_routes) > 0:
            raise ValueError(f"Missing routes: {remaining_routes}")
        return route_mapping

    async def _transform(
        self,
        source: bytes | str,
        query: str | None = None,
        skip_routing: bool = False,
        **kwargs: Any,
    ) -> str | bytes:
        """Converts an image input to a target modality using the routed converter.

        Args:
            source (bytes | str): The image to be converted, provided as raw bytes or path.
            query (str | None): Optional query string to guide the transformation.
            skip_routing (bool): If True, it will skip the routing process. default to False.
            kwargs (Any): Additional arguments passed to the converter.

        Returns:
            str | bytes: The transformed result, typically text or another modality format.
        """
        selected_route = self.router.route(source) if not skip_routing else self.router.default_route
        converter = self.route_mapping[selected_route]
        result: TextResult = await converter.convert(source, query, **kwargs)
        return result.result

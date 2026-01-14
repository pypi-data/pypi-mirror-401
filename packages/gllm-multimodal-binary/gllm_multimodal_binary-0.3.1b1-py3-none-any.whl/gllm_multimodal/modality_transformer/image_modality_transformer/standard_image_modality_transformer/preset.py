"""This module defines a standard modality transformer that converts images into text/bytes via route.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

Reference:
    NONE
"""

from gllm_pipeline.router import LMBasedRouter
from gllm_pipeline.router.router import BaseRouter

from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption
from gllm_multimodal.modality_converter.image_to_text.image_to_mermaid import LMBasedImageToMermaid
from gllm_multimodal.modality_converter.modality_converter import BaseModalityConverter


def get_preset(preset_name: str = "domain_specific") -> dict[str, BaseRouter | dict[str, BaseModalityConverter]]:
    """Get the preset configuration for standard transformer.

    Args:
        preset_name (str): The name of the preset to get.

    Returns:
        dict[str, BaseRouter | dict[str, BaseModalityConverter]]: A tuple containing router and route mapping.
    """
    if preset_name == "domain_specific":
        router = LMBasedRouter.from_preset(input_modality_type="image", preset_name=preset_name)
        default_i2c_converter = LMBasedImageToCaption.from_preset()
        default_i2m_converter = LMBasedImageToMermaid.from_preset()
        return {
            "router": router,
            "route_mapping": {
                "general_image": default_i2c_converter,
                "engineering_diagram": default_i2c_converter,
                "healthcare_x_ray": default_i2c_converter,
                "healthcare_mri_ct_scan": default_i2c_converter,
                "diagram": default_i2m_converter,
                "organizational_chart": default_i2m_converter,
            },
        }
    else:
        raise ValueError("Invalid preset_name.")

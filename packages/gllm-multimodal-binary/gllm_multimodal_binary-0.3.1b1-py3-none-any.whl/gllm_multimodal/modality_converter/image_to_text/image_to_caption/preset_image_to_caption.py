"""This module provides a preset configuration for generating image captions.

Authors:
    Yanfa Adi Putra (yanfa.adi.putra@gdplabs.id)

References:
    None
"""

import os

from gllm_inference.builder import build_lm_invoker
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.output_parser import JSONOutputParser
from gllm_inference.output_parser.output_parser import BaseOutputParser
from gllm_inference.prompt_builder import PromptBuilder

# TODO: adjust language as param
DEFAULT_SYSTEM_PROMPT = """
    <INSTRUCTIONS>
    Create {number_of_captions} captions in Indonesian.
    You will be given several images.
    The main image is the one that needs captions.
    The other images are used as context.
    Make sure every name or technical term remains in its original language in the context.

    <OUTPUT_FORMAT>
    Provide the captions in JSON format without any additions:
    ```
    {{
    "captions": [
        "<caption_1>",
        "<caption_2>",
        "<caption_3>",
        ...
    ]
    }}
    </OUTPUT_FORMAT>
    </INSTRUCTIONS>
"""

DEFAULT_USER_PROMPT = """
    <INPUT_STRUCTURE>
    Title: {image_one_liner}
    Content: {image_description}
    Main Image Filename: {filename}
    Metadata: {image_metadata}
    Injected Domain Knowledge: {domain_knowledge}
    </INPUT_STRUCTURE>
"""


def create_default_prompt_builder() -> PromptBuilder:
    """Create a default prompt builder with templates for generating image captions.

    This function creates and returns an PromptBuilder instance configured with
    default templates for image captioning tasks. The templates are structured to:

    System prompt:
    1. Instructs the model to generate the specified number of captions.
    2. Specifies output format as a JSON list of captions.

    User prompt:
    1. Provides structured input format with fields for:
        1. Image one-liner
        2. Image description
        3. Domain knowledge (will be generated from the image given)
        4. Filename (will be generated from the image given)
        5. Image metadata (will be generated from the image given)

    Returns:
        PromptBuilder: A prompt builder instance configured with default
            templates for image captioning.
    """
    system_prompt = DEFAULT_SYSTEM_PROMPT
    user_prompt = DEFAULT_USER_PROMPT

    return PromptBuilder(system_template=system_prompt, user_template=user_prompt)


# TODO: Adjust to a stand alone preset
def get_preset_image_to_caption(
    preset_name: str | None,
) -> tuple[BaseLMInvoker, PromptBuilder, BaseOutputParser]:
    """Get the preset configuration for generating image captions.

    Args:
        preset_name (str): The name of the preset to get.

    Returns:
        tuple[BaseLMInvoker, PromptBuilder, BaseOutputParser]: A tuple containing the preset
            configuration for image captioning.
    """
    if preset_name is None or preset_name == "default":
        model_id = os.getenv("DEFAULT_IMAGE_CAPTIONING_MODEL_ID", "google/gemini-2.5-flash")
        return (
            build_lm_invoker(model_id=model_id),
            create_default_prompt_builder(),
            JSONOutputParser(),
        )

    raise ValueError(f"Invalid preset name: {preset_name}")

"""LM-based image captioning implementation using multimodal Language Models.

This module implements image captioning using multimodal Language Models
through the lm_invoker package.

Authors:
    Yanfa Adi Putra (yanfa.a.putra@gdplabs.id)

References:
    NONE
"""

from typing import Any

from gllm_inference.request_processor.lm_request_processor import LMRequestProcessor
from gllm_inference.request_processor.uses_lm_mixin import UsesLM
from gllm_inference.schema.attachment import Attachment

from gllm_multimodal.constants import (
    CaptionConstants,
    ImageToTextConstants,
)
from gllm_multimodal.modality_converter.image_to_text.image_to_caption.image_to_caption import BaseImageToCaption
from gllm_multimodal.modality_converter.image_to_text.image_to_caption.preset_image_to_caption import (
    get_preset_image_to_caption,
)
from gllm_multimodal.modality_converter.schema.caption import Caption


class LMBasedImageToCaption(BaseImageToCaption, UsesLM):
    """Image captioning implementation using Language Models.

    This class implements the ImageToCaption interface using LMs for generating
    natural language captions.
    """

    def __init__(self, lm_request_processor: LMRequestProcessor):
        """Initialize the LM based image captioning component.

        Args:
            lm_request_processor: Language model request processor instance that supports multimodal inputs.
            prompt_builder: Base prompt builder for constructing model inputs. For best results,
                the prompt should include all of the following placeholders in curly braces {}:
                1. filename: Name of the image file.
                2. number_of_captions: Number of captions to generate.
                3. image_oneliner: Brief one-line summary.
                4. image_description: Detailed description.
                5. domain_knowledge: Domain-specific context.
                6. metadata: Image metadata as JSON string.
            event_emitter: Optional event emitter for streaming responses.
            caption_json_key: Key in the JSON response containing captions. Defaults to 'captions'.
        """
        super().__init__()
        self.lm_request_processor = lm_request_processor

    @classmethod
    def from_preset(
        cls,
        preset_name: str | None = "default",
        **kwargs: Any,
    ) -> "LMBasedImageToCaption":
        """Initialize the LM based image captioning component using preset model configurations.

        Args:
            preset_name (str): Name of the preset to use.
            **kwargs (Any): Additional keyword arguments to pass to from_lm_components().

        Returns:
            LMBasedImageToCaption: Initialized image captioning component using preset model.
        """
        lm_invoker, prompt_builder, output_parser = get_preset_image_to_caption(preset_name)
        return cls.from_lm_components(prompt_builder, lm_invoker, output_parser, **kwargs)

    async def _get_captions(
        self,
        image_binary: bytes,
        filename: str,
        caption_data: Caption,
        **kwargs: Any,
    ) -> list[str]:
        """Generate image captions using a Large Vision Language Model.

        Args:
            image_binary (bytes): Raw binary data of the image to caption.
            filename (str): Name of the image file, used for reference.
            caption_data (Caption): Caption data containing:
                1. image_oneliner (str, optional): Brief one-line summary or title (default: "Not given").
                2. image_description (str, optional): Detailed description of the image (default: "Not given").
                3. domain_knowledge (str, optional): Relevant domain-specific information (default: "Not given").
                4. image_metadata (dict[str, Any], optional): Image metadata EXIF for data GPS coordinates if available.
                5. number_of_captions (int, optional): Number of captions to generate (default: 5).
            **kwargs (Any): Additional keyword arguments to pass.

        Returns:
            list[str]: A list of generated captions.

        Note:
            The method expects the LVLM to return a JSON response with the following structure:
            {
                "captions": [
                    "caption1",
                    "caption2",
                    ...
                ]
            }
        """
        try:
            prompt_key_set = self.lm_request_processor.prompt_builder.prompt_key_set

            number_of_captions = caption_data.number_of_captions
            param_mapping = {
                ImageToTextConstants.FILENAME: filename if filename else ImageToTextConstants.NO_IMAGE_FILENAME,
                **caption_data.model_dump(),
            }

            prompt_params = {key: value for key, value in param_mapping.items() if key in prompt_key_set}

            attachments = [Attachment.from_bytes(image_binary)] + caption_data.attachments_context
            response = await self.lm_request_processor.process(
                prompt_kwargs=prompt_params,
                extra_contents=attachments,
                event_emitter=kwargs.get("event_emitter", None),
            )

            captions = response[CaptionConstants.CAPTION_DEFAULT_JSON_KEY]
            if len(captions) < number_of_captions:
                self._logger.debug(f"Generated {len(captions)} captions, but expected {number_of_captions}")

            return captions

        except Exception as e:
            self._logger.debug(f"Failed to generate captions will return empty list, details: {str(e)}")
            return []

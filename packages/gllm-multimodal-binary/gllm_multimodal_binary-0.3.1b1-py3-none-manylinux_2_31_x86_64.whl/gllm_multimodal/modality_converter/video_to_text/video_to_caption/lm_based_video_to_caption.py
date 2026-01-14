"""LM-based video captioning implementation using multimodal Language Models.

This module implements video captioning using multimodal Language Models
through the lm_invoker package.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

from typing import Any

from gllm_inference.exceptions import BaseInvokerError
from gllm_inference.lm_invoker import GoogleLMInvoker
from gllm_inference.request_processor.lm_request_processor import LMRequestProcessor
from gllm_inference.request_processor.uses_lm_mixin import UsesLM
from gllm_inference.schema import Attachment

from gllm_multimodal.constants import ImageToTextConstants
from gllm_multimodal.modality_converter.schema.caption import Caption
from gllm_multimodal.modality_converter.video_to_text.video_to_caption.preset_video_to_caption import (
    get_preset_video_to_caption,
)
from gllm_multimodal.modality_converter.video_to_text.video_to_caption.video_to_caption import (
    BaseVideoToCaption,
)

DEFAULT_FILENAME = "video.mp4"


class LMBasedVideoToCaption(BaseVideoToCaption, UsesLM):
    """Video captioning implementation using Language Models.

    This class implements the VideoToCaption interface using LMs for generating
    natural language captions.
    """

    def __init__(self, lm_request_processor: LMRequestProcessor):
        """Initialize the LM based video captioning component.

        Args:
            lm_request_processor: Language model request processor instance that supports multimodal inputs.
        """
        super().__init__()
        self.lm_request_processor = lm_request_processor

    @classmethod
    def from_preset(
        cls,
        preset_name: str | None = "default",
        **kwargs: Any,
    ) -> "LMBasedVideoToCaption":
        """Initialize the LM based video captioning component using preset model configurations.

        Args:
            preset_name (str): Name of the preset to use.
            **kwargs (Any): Additional keyword arguments to pass to from_lm_components().

        Returns:
            LMBasedVideoToCaption: Initialized video captioning component using preset model.
        """
        lm_invoker, prompt_builder, output_parser = get_preset_video_to_caption(preset_name)
        return cls.from_lm_components(prompt_builder, lm_invoker, output_parser, **kwargs)

    def _build_prompt_params(self, video_attachment: Attachment, caption_data: Caption) -> dict[str, Any]:
        """Build prompt parameters from caption data.

        Args:
            video_attachment (Attachment): The video attachment containing filename and other metadata.
            caption_data (Caption): Caption data containing metadata and configuration.

        Returns:
            dict[str, Any]: Filtered prompt parameters matching the prompt builder's key set.
        """
        prompt_key_set = self.lm_request_processor.prompt_builder.prompt_key_set

        filename = video_attachment.filename or DEFAULT_FILENAME
        param_mapping = {
            ImageToTextConstants.FILENAME: filename,
            **caption_data.model_dump(),
        }

        return {key: value for key, value in param_mapping.items() if key in prompt_key_set}

    async def _get_captions(
        self,
        video_attachment: Attachment,
        caption_data: Caption,
        **kwargs: Any,
    ) -> dict[str, str | list[dict[str, Any]]]:
        """Generate video captions using a Large Vision Language Model.

        Args:
            video_attachment (Attachment): The video attachment containing:
                - data (bytes): Raw binary data of the video
                - filename (str): Name of the video file
                - mime_type (str): MIME type of the video
                - extension (str): File extension
            caption_data (Caption): Caption data containing:
                1. title (str, optional): Brief one-line summary or title (default: "Not given").
                2. description (str, optional): Detailed description of the video (default: "Not given").
                3. domain_knowledge (str, optional): Relevant domain-specific information (default: "Not given").
                4. metadata (dict[str, Any], optional): Video metadata if available.
                5. number_of_captions (int, optional): Number of captions to generate (default: 5).
            **kwargs (Any): Additional keyword arguments to pass.

        Returns:
            dict[str, str | list[dict[str, Any]]]: A dictionary of extracted video captioning.

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
            prompt_params = self._build_prompt_params(video_attachment, caption_data)

            response = await self.lm_request_processor.process(
                prompt_kwargs=prompt_params,
                extra_contents=[video_attachment] + caption_data.attachments_context,
                event_emitter=kwargs.get("event_emitter"),
            )
            return response
        except ValueError as e:
            self._logger.error(f"Invalid video data: {str(e)}")
            raise
        except BaseInvokerError as e:
            self._logger.error(f"Failed to generate captions: {str(e)}")
            return {}
        except Exception as e:
            self._logger.exception(f"Unexpected error during caption generation: {str(e)}")
            return {}

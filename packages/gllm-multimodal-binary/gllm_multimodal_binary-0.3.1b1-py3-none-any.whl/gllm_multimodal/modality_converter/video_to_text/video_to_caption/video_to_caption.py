"""Base class for video captioning implementations in Gen AI applications.

This module provides the foundation for converting videos to natural language captions.
It supports various types of captioning:
1. Video summaries
2. Event segmentation with captions
3. Keyframe descriptions
4. Transcript integration

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_inference.schema import Attachment

from gllm_multimodal.modality_converter.schema.caption import Caption
from gllm_multimodal.modality_converter.schema.text_result import TextResult
from gllm_multimodal.modality_converter.schema.video_caption_result import (
    Segment,
    VideoCaptionMetadata,
)
from gllm_multimodal.modality_converter.video_to_text.video_to_text import BaseVideoToText
from gllm_multimodal.utils.image_utils import get_image_binary


class BaseVideoToCaption(BaseVideoToText, ABC):
    """Abstract base class for video captioning operations in Gen AI applications.

    This class extends BaseVideoToText to provide specialized functionality for generating
    captions from videos. It supports video segmentation, keyframe extraction, transcript
    integration, and can incorporate additional context like video title, description,
    domain knowledge, and metadata.
    """

    async def _convert(
        self,
        source: str | Attachment,
        **kwargs: Any,
    ) -> TextResult:
        """Convert a video to natural language captions with structured output.

        This method orchestrates the complete video captioning process:
        1. Loads and validates the video from the source
        2. Generates captions for the video
        3. Constructs the structured result with segments, transcripts, and keyframes

        Args:
            source (str | Attachment): The source of the video, which can be:
                1. A file path to a local video
                2. A URL pointing to a video
                3. A base64 encoded video string
                4. An S3 URL for videos stored in AWS S3
                5. An Attachment object containing video bytes
            **kwargs (Any): Additional keyword arguments including:
                1. number_of_captions (int, optional): Number of captions to generate (default: 5).
                2. title (str, optional): Brief one-line summary or title (default: "Not given").
                3. description (str, optional): Detailed description of the video (default: "Not given").
                4. domain_knowledge (str, optional): Relevant domain-specific information (default: "Not given").
                5. attachments_context (list[bytes | Attachment], optional): A list of attachment formatted
                    as Attachment or bytes.
                6. use_metadata (bool, optional): Whether to use video metadata (default: True).

        Returns:
            TextResult: A structured result containing:
                1. result: Video summary as a single string.
                2. metadata: A VideoCaptionMetadata object containing:
                    1. video_summary: Brief summary of the entire video.
                    2. segments: List of Segment objects with captions, keyframes, and transcripts.

        Raises:
            ValueError: If the video source is invalid or inaccessible
            RuntimeError: If caption generation fails
        """
        if isinstance(source, Attachment):
            video_attachment = source
        else:
            # TODO: change to `get_binary` instead of `get_image_binary`
            video_binary, filename = await get_image_binary(source)
            if video_binary is None:
                raise ValueError("Failed to load video from source")
            video_attachment = Attachment.from_bytes(video_binary, filename=filename)

        delete_attachments_context = kwargs.get("delete_attachments_context", True)

        caption_data = Caption(**kwargs)

        video_caption = await self._get_captions(
            video_attachment=video_attachment,
            caption_data=caption_data,
            **kwargs,
        )

        if delete_attachments_context:
            caption_data.attachments_context = []

        segments = self._build_segments(video_caption.get("segments", []))

        video_metadata = VideoCaptionMetadata(
            video_summary=video_caption.get("video_summary"),
            segments=segments,
        )

        return TextResult(
            result=video_caption.get("video_summary"), tag="caption", metadata=video_metadata.model_dump()
        )

    def _build_segments(self, segments_data: list[dict[str, Any]]) -> list[Segment]:
        """Build Segment objects from segment data dictionaries.

        This method leverages the Segment model's built-in validation to ensure
        each segment has a caption. The Segment.ensure_caption() validator will
        automatically populate segment_caption from keyframes or transcripts if needed.

        Args:
            segments_data (list[dict[str, Any]]): List of segment dictionaries.

        Returns:
            list[Segment]: List of constructed and validated Segment objects.
        """
        return [Segment(**seg_data) for seg_data in segments_data]

    @abstractmethod
    async def _get_captions(
        self,
        video_attachment: Attachment,
        caption_data: Caption,
        **kwargs: Any,
    ) -> dict[str, str | list[dict[str, Any]]]:
        """Generate video captions using provided context and configuration.

        This abstract method must be implemented by subclasses to define the specific
        caption generation logic. The implementation should consider all provided context
        and adhere to the specified captioning standards.

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
            dict[str, str | list[dict[str, Any]]]: A dictionary containing:
                - video_summary (str): Summary of the entire video
                - segments (list[dict]): List of segment dictionaries with fields:
                    - start_time (float): Segment start time
                    - end_time (float): Segment end time
                    - transcripts (list[dict]): Transcript entries
                    - keyframes (list[dict]): Keyframe descriptions
                    - segment_caption (list[str], optional): Captions for the segment

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
            ValueError: If the video data is invalid or cannot be processed.
        """
        raise NotImplementedError

"""Schema definitions for image-to-text operations."""

from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript
from gllm_multimodal.modality_converter.schema.caption import Caption
from gllm_multimodal.modality_converter.schema.text_result import TextResult

__all__ = [
    "AudioTranscript",
    "Caption",
    "TextResult",
]

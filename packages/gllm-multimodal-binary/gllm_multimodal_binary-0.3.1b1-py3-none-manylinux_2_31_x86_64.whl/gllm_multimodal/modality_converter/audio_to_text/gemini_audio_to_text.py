"""Defines a module to convert video to text using Gemini Video Understanding.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    [1] https://ai.google.dev/gemini-api/docs/video-understanding

Todo:
    - Standardize output format to use TextResult from gllm_multimodal.modality_converter.schema.text_result.py.
    - ARCHITECTURAL CONSIDERATION - Consider moving this out of audio_to_text module. This class is currently in the
        "audio_to_text" module, while the Gemini API supports both audio and video processing in a unified way.
"""

import os

from gllm_core.utils.logger_manager import LoggerManager
from gllm_core.utils.retry import RetryConfig
from gllm_inference.lm_invoker import GoogleLMInvoker
from gllm_inference.schema import Attachment, Message
from pydantic import BaseModel

from gllm_multimodal.modality_converter.audio_to_text.audio_to_text import BaseAudioToText
from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript
from gllm_multimodal.utils.audio_to_text_utils import is_youtube_url

DEFAULT_SYSTEM_PROMPT = """You are a transcription assistant.

Your job is to convert audio into structured transcripts.

Output format:
- Always return at least one item in 'audio_transcripts'.
- Each item must include: text, start_time (sec), end_time (sec), lang_id.
- Segments must be chronological, with no gaps or overlaps.

Guidelines:
1. Write speech verbatim with correct punctuation and casing.
2. Start a new segment on speaker change, using "Speaker N:".
3. For non-speech (silence, music, noise, visuals), add a segment starting with "Non-speech:", set lang_id=null.
4. If audio is unclear, mark it with "[inaudible]" or "[crosstalk]".
5. Use ISO 639-1 codes for lang_id (e.g., 'en', 'id'); use null if unknown.
6. Align timestamps closely with actual speech boundaries.
7. Never invent or alter speech; preserve original meaning.
"""  # noqa: E501


DEFAULT_USER_PROMPT = "Please transcribe the audio from the attached media file."


class AudioTranscripts(BaseModel):
    """Schema for audio transcripts response from Gemini API."""

    audio_transcripts: list[AudioTranscript] = []


class GeminiAudioToText(BaseAudioToText):
    """A audio to text converter using Gemini."""

    def __init__(  # noqa: PLR0913
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        user_prompt: str = DEFAULT_USER_PROMPT,
        max_retries: int = 0,
        timeout: float = 0,
    ):
        """Initializes the GeminiAudioToText.

        Args:
            api_key (str): The API key for the Gemini API.
            model (str, optional): The model to use for the audio to text conversion. Defaults to "gemini-2.5-flash".
            system_prompt (str, optional): Custom system prompt for audio processing. Defaults to DEFAULT_SYSTEM_PROMPT.
            user_prompt (str, optional): Custom user prompt for audio processing. Defaults to DEFAULT_USER_PROMPT.
            max_retries (int, optional): The maximum number of retry attempts for failed requests. Defaults to 0.
            timeout (float, optional): The timeout duration for requests in seconds. Defaults to 0 (no timeout).
        """
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.client = GoogleLMInvoker(
            api_key=api_key,
            model_name=model,
            response_schema=AudioTranscripts,
            retry_config=RetryConfig(max_retries=max_retries, timeout=timeout),
        )

        self.logger = LoggerManager().get_logger(self.__class__.__name__)

    async def convert(self, audio_source: str) -> list[AudioTranscript]:
        """Converts an audio source to text.

        Args:
            audio_source (str): The path to the audio file. Can be:
                - file path to a local audio file
                - a YouTube URL

        Returns:
            list[AudioTranscript]: A list of AudioTranscript.

        Raises:
            ValueError: If the provided audio source is not supported or cannot be processed.
        """
        self.logger.debug(f"Converting audio source: {audio_source}")

        if is_youtube_url(audio_source):
            file = Attachment.from_url(url=audio_source)

        elif os.path.exists(audio_source) and os.path.isfile(audio_source):
            self.logger.debug(f"Audio source is a local file: {audio_source}")
            file = Attachment.from_path(path=audio_source)

        else:
            raise ValueError(f"Invalid audio source: {audio_source}.")

        self.logger.debug(
            f"Generating content using model: {self.model}, "
            f"system prompt: {self.system_prompt}, user prompt: {self.user_prompt}"
        )

        invoker_prompt: list[Message] = [
            Message.system(self.system_prompt),
            Message.user([file, self.user_prompt]),
        ]
        response = await self.client.invoke(invoker_prompt)
        audio_transcripts = response.structured_output.audio_transcripts

        self.logger.debug(f"Successfully generated {len(audio_transcripts)} audio transcripts.")

        return audio_transcripts

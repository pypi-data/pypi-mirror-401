"""Defines a module to convert audio to text using OpenAI Whisper.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)
    Devita (devita1@gdplabs.id)

References:
    [1] https://platform.openai.com/docs/guides/speech-to-text
    [2] https://platform.openai.com/docs/api-reference/audio/createTranscription

Todo:
    - Standardize output format to use TextResult from gllm_multimodal.modality_converter.schema.text_result.py.
"""

from io import BytesIO

import numpy as np
import soundfile as sf
from gllm_core.utils.logger_manager import LoggerManager
from langcodes import find_name
from openai import OpenAI
from openai.types.audio import TranscriptionVerbose
from scipy import signal

from gllm_multimodal.modality_converter.audio_to_text.audio_to_text import BaseAudioToText
from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript
from gllm_multimodal.utils.audio_to_text_utils import (
    convert_audio_to_mono_flac,
    detect_audio_format,
    get_audio_from_base64,
    get_audio_from_downloadable_url,
    get_audio_from_file_path,
    get_audio_from_youtube_url,
)

MAX_AUDIO_SIZE = 25 * 1024 * 1024  # 25 MB

AUDIO_FORMAT_TO_MIME_TYPE = {
    "mp3": "audio/mpeg",
    "mpeg": "audio/mpeg",
    "mpga": "audio/mpeg",
    "m4a": "audio/mp4",
    "wav": "audio/wav",
    "wave": "audio/wav",
    "flac": "audio/flac",
    "ogg": "audio/ogg",
    "oga": "audio/ogg",
}


class OpenAIWhisperAudioToText(BaseAudioToText):
    """An audio to text converter using OpenAI Whisper.

    The OpenAIWhisperAudioToText class is responsible for converting audio to text using OpenAI Whisper.
    It supports various audio sources such as file paths, base64 encoded strings, downloadable audio URLs,
    and YouTube URLs.

    Attributes:
        client (OpenAI): The OpenAI client instance used for API requests.
        model (str): The identifier of the OpenAI Whisper model to use for transcription.
        language (str | None): The language of the input audio content.
        prompt (str | None): The text prompt to guide the model's style or continue a previous audio segment.
        temperature (float): The sampling temperature to control output randomness.
        timestamp_granularity (str): The timestamp detail levels to include in the output.
        proxy (str | None): The proxy URL to use for the YouTube request.
        skip_conversion_for_formats (list[str]): List of audio formats that should skip mono FLAC conversion.
    """

    # ruff: noqa: PLR0913
    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        api_key: str,
        model: str = "whisper-1",
        language: str | None = None,
        prompt: str | None = None,
        temperature: float = 0,
        timestamp_granularity: str = "segment",
        proxy: str | None = None,
        skip_conversion_for_formats: list[str] | None = None,
    ):
        """Initialize the OpenAIWhisperAudioToText instance.

        Args:
            api_key (str): The API key for authentication with OpenAI.
            model (str, optional): The model identifier to use for transcription. Defaults to "whisper-1".
            language (str | None, optional): The language of the input audio content. Defaults to None.
            prompt (str | None, optional): The text prompt to guide the model's style or continue a previous audio
                segment. The prompt should match the audio language. Defaults to None.
            temperature (float, optional): The sampling temperature to control output randomness. Defaults to 0.
            timestamp_granularity (str, optional): The timestamp detail levels to include in the output.
                The granularity can be "segment" or "word". When set to "segment", OpenAI will return
                transcripts divided into segments of speech. When set to "word", it will include word-level
                timestamps. Defaults to "segment".
            proxy (str | None, optional): The proxy URL to use for the YouTube request. Defaults to None.
            skip_conversion_for_formats (list[str] | None, optional): List of audio formats (e.g., ['mp3', 'wav'])
                that should skip the mono FLAC conversion process. Formats are case-insensitive and can be
                specified with or without a leading dot. If None or empty, all audio will be converted to
                mono FLAC. Defaults to None.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.language = language
        self.prompt = prompt
        self.temperature = temperature
        self.timestamp_granularity = timestamp_granularity
        self.proxy = proxy
        self.skip_conversion_for_formats = [fmt.lower().strip(".") for fmt in (skip_conversion_for_formats or [])]
        self.logger = LoggerManager().get_logger(self.__class__.__name__)

    async def convert(self, audio_source: str) -> list[AudioTranscript]:
        """Convert audio to text using OpenAI Whisper.

        This method process the given audio source and return a list of AudioTranscript.
        The audio source can be a file path, a base64 encoded string, or a URL.

        Args:
            audio_source (str): The source of the audio to convert. Can be:
                - A file path to an audio file.
                - A base64 encoded string of the audio.
                - A downloadable audio URL (e.g. Google Drive, OneDrive).
                - A YouTube URL.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript.

        Raises:
            ValueError: If the provided audio source is not supported or cannot be processed.
        """
        self.logger.debug("Converting audio source: %s", audio_source)

        # if audio source is audio file path
        if audio_binary_data := get_audio_from_file_path(audio_source):
            self.logger.debug("Audio source is a valid audio file path: %s", audio_source)
            return self._transcribe_audio_file(audio_binary_data)

        # if audio source is base64 encoded string
        if audio_binary_data := get_audio_from_base64(audio_source):
            self.logger.debug("Audio source is a valid base64 encoded audio string: %s", audio_source)
            return self._transcribe_audio_file(audio_binary_data)

        # if audio source is downloadable audio URL
        if audio_binary_data := get_audio_from_downloadable_url(audio_source):
            self.logger.debug("Audio source is a valid downloadable audio URL: %s", audio_source)
            return self._transcribe_audio_file(audio_binary_data)

        # if audio source is youtube URL
        if audio_binary_data := get_audio_from_youtube_url(audio_source, self.proxy):
            self.logger.debug("Audio source is a valid YouTube URL: %s", audio_source)
            return self._transcribe_audio_file(audio_binary_data)

        raise ValueError("Unsupported audio source")

    def _transcribe_audio_file(self, audio: bytes) -> list[AudioTranscript]:
        """Transcribe the audio file using OpenAI Whisper.

        This method transcribes the audio and returns the transcription results as AudioTranscript objects.
        If the audio format is in the skip list, the conversion to mono FLAC is bypassed.

        Args:
            audio (bytes): Bytes containing the audio data.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects containing the transcribed audio.
        """
        audio_format = detect_audio_format(audio)
        should_skip_conversion = audio_format and audio_format in self.skip_conversion_for_formats

        if should_skip_conversion:
            self.logger.debug("Skipping audio conversion for format: %s", audio_format)
            processed_audio = audio
            audio_mime_type = AUDIO_FORMAT_TO_MIME_TYPE.get(audio_format, f"audio/{audio_format}")
            audio_extension = audio_format
        else:
            self.logger.debug("Converting audio to mono FLAC format")
            processed_audio = convert_audio_to_mono_flac(audio)
            audio_mime_type = "audio/flac"
            audio_extension = "flac"

        file_size = len(processed_audio)

        if file_size > MAX_AUDIO_SIZE:
            self.logger.debug(
                "Audio file size %d bytes exceeds the maximum allowed size: %d bytes", file_size, MAX_AUDIO_SIZE
            )
            if should_skip_conversion:
                raise ValueError(
                    f"Audio file size ({file_size / (1024 * 1024):.2f} MB) exceeds the maximum allowed size "
                    f"({MAX_AUDIO_SIZE / (1024 * 1024):.2f} MB). Conversion was skipped for format '{audio_format}' "
                    f"as specified in skip_conversion_for_formats. Please provide a smaller audio file or remove "
                    f"'{audio_format}' from skip_conversion_for_formats to enable automatic size reduction."
                )
            else:
                processed_audio = self._reduce_file_size(processed_audio)

        audio_file = (f"audio.{audio_extension}", BytesIO(processed_audio), audio_mime_type)

        self.logger.debug("Transcribing audio file: %s", audio_file[0])

        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
            language=self.language,
            prompt=self.prompt,
            response_format="verbose_json",
            temperature=self.temperature,
            timestamp_granularities=[self.timestamp_granularity],
        )

        self.logger.debug(
            "Received transcription response with %d segments/words",
            len(getattr(transcription, "segments", []) or []) + len(getattr(transcription, "words", []) or []),
        )

        return self._convert_whisper_response_to_audio_transcripts(transcription)

    def _reduce_file_size(self, audio_bytes: bytes) -> bytes:
        """Progressively reduce audio quality until file size is under limit.

        Args:
            audio_bytes (bytes): The audio file as bytes.

        Returns:
            bytes: Reduced size audio file as bytes.
        """
        with sf.SoundFile(BytesIO(audio_bytes)) as audio:
            data = audio.read()
            samplerate = audio.samplerate

        # Quality reduction steps
        steps = [
            {"sample_rate": 16000, "channels": 1, "bit_depth": 16},  # Step 1: 16kHz, mono, 16-bit
            {"sample_rate": 8000, "channels": 1, "bit_depth": 16},  # Step 2: 8kHz, mono, 16-bit
            {"sample_rate": 4000, "channels": 1, "bit_depth": 16},  # Step 3: 4kHz, mono, 16-bit
            {"sample_rate": 2000, "channels": 1, "bit_depth": 16},  # Step 4: 2kHz, mono, 16-bit
        ]

        for step in steps:
            # Resample if needed
            if step["sample_rate"] != samplerate:
                # Calculate number of samples for new sample rate
                num_samples = int(len(data) * step["sample_rate"] / samplerate)
                data = signal.resample(data, num_samples)
                samplerate = step["sample_rate"]

            # Convert to mono if needed
            if step["channels"] == 1 and len(data.shape) > 1:
                data = np.mean(data, axis=1)

            # Convert bit depth
            if step["bit_depth"] == 16:  # noqa: PLR2004
                data = (data * 32767).astype(np.int16)  # 2^15 - 1 = 32767, maximum value for 16-bit audio

            output = BytesIO()
            sf.write(output, data, samplerate, format="FLAC", subtype="PCM_16")
            reduced_bytes = output.getvalue()
            output.close()

            size = len(reduced_bytes)
            self.logger.debug(
                f"Reduced size with {step}: {size / (1024 * 1024):.2f} MB "
                f"(SR: {step['sample_rate']}Hz, Ch: {step['channels']}, "
                f"Depth: {step['bit_depth']}-bit)"
            )

            if size <= MAX_AUDIO_SIZE:
                return reduced_bytes

        raise ValueError("Unable to reduce file size below limit even with lowest quality settings")

    def _convert_whisper_response_to_audio_transcripts(
        self, transcription: TranscriptionVerbose
    ) -> list[AudioTranscript]:
        """Convert the OpenAI Whisper response to a list of AudioTranscript.

        This method processes the OpenAI Whisper response and returns a list of AudioTranscript objects.
        The response contains transcribed segments and/or words with their timestamps. The method extracts
        the language information and combines all transcribed elements into a unified list of transcripts.

        Args:
            transcription (TranscriptionVerbose): The OpenAI Whisper transcription response object
                containing segments, words, language, and other information.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects, each containing the text,
                start_time, end_time, and lang_id.
        """
        lang_id = self._convert_language_to_iso_639(transcription.language) if transcription.language else None
        audio_transcripts = []

        # Process segments
        for segment in transcription.segments or []:
            audio_transcripts.append(
                AudioTranscript(
                    text=segment.text,
                    start_time=segment.start,
                    end_time=segment.end,
                    lang_id=lang_id,
                )
            )

        # Process words
        for word in transcription.words or []:
            audio_transcripts.append(
                AudioTranscript(
                    text=word.word,
                    start_time=word.start,
                    end_time=word.end,
                    lang_id=lang_id,
                )
            )

        return audio_transcripts

    def _convert_language_to_iso_639(self, language: str) -> str | None:
        """Convert the language to the ISO 639 code.

        Args:
            language (str): The language to convert.

        Returns:
            str | None: The ISO 639 code. If the language is not found, return None.
        """
        try:
            return find_name("language", language).language
        except LookupError:
            self.logger.debug("Failed to convert language: %s to ISO 639 code", language)
            return None

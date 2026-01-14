"""Defines a module to convert audio to text using Google Cloud Speech-to-Text.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    [1] https://cloud.google.com/speech-to-text/docs/async-recognize#speech-async-recognize-gcs-python
    [2] https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages

Todo:
    - Standardize output format to use TextResult from gllm_multimodal.modality_converter.schema.text_result.py.
"""

import uuid

from gllm_core.utils.logger_manager import LoggerManager
from google.cloud import storage
from google.cloud.speech import RecognitionAudio, RecognitionConfig, RecognizeResponse, SpeechClient
from google.oauth2.service_account import Credentials
from langcodes import Language
from langcodes.tag_parser import LanguageTagError

from gllm_multimodal.modality_converter.audio_to_text.audio_to_text import BaseAudioToText
from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript
from gllm_multimodal.utils.audio_to_text_utils import (
    convert_audio_to_mono_flac,
    get_audio_duration,
    get_audio_from_base64,
    get_audio_from_downloadable_url,
    get_audio_from_file_path,
    get_audio_from_youtube_url,
)

MAX_AUDIO_DURATION = 60


class GoogleCloudAudioToText(BaseAudioToText):
    """An audio to text converter using Google Cloud Speech-to-Text.

    The GoogleCloudAudioToText class is responsible for converting audio to text using the Google Cloud Speech-to-Text.
    It supports various audio input formats and can handle audio from local files, base64 encoded strings,
    or URLs pointing to audio files.

    Attributes:
        speech_client (SpeechClient): Google Cloud Speech-to-Text client.
        storage_client (storage.Client): Google Cloud Storage client.
        bucket_name (str): Google Cloud Storage bucket name.
        language_code (str): Language code for transcription.
        alternative_language_codes (list[str] | None): Alternative language codes for transcription.
            Up to 3 alternatives.
        model (str): Transcription model name.
        timeout (int): Timeout for the transcription request.
        proxy (str | None): The proxy URL to use for the YouTube request.
    """

    # ruff: noqa: PLR0913
    def __init__(
        self,
        credentials_json: str | dict,
        bucket_name: str,
        language_code: str = "id-ID",
        alternative_language_codes: list[str] | None = None,
        model: str = "latest_long",
        timeout: int = 5 * 60,
        proxy: str | None = None,
    ):
        """Initialize the GoogleCloudAudioToText instance.

        Args:
            credentials_json (str | dict): Google Cloud API credentials can either be a file path or a dictionary.
            bucket_name (str): Google Cloud Storage bucket name.
            language_code (str, optional): Language code for transcription. Defaults to "id-ID".
            alternative_language_codes (list[str] | None, optional): Alternative language codes for transcription.
                Up to 3 alternatives. If the list has more than 3 elements, the first 3 will be used.
                Defaults to None, in which ["id-ID", "en-US", "en-GB"] is used.
            model (str, optional): Transcription model name. Defaults to "latest_long".
            timeout (int, optional): Timeout for the transcription request. Defaults to 5 minutes.
            proxy (str | None, optional): The proxy URL to use for the YouTube request. Defaults to None.
        """
        credentials = (
            Credentials.from_service_account_file(credentials_json)
            if isinstance(credentials_json, str)
            else Credentials.from_service_account_info(credentials_json)
        )

        self.speech_client = SpeechClient(credentials=credentials)
        self.storage_client = storage.Client(credentials=credentials)
        self.bucket_name = bucket_name
        self.language_code = language_code
        self.alternative_language_codes = (
            ["id-ID", "en-US", "en-GB"] if alternative_language_codes is None else alternative_language_codes[:3]
        )
        self.model = model
        self.timeout = timeout
        self.proxy = proxy
        self.logger = LoggerManager().get_logger(self.__class__.__name__)

    async def convert(self, audio_source: str) -> list[AudioTranscript]:
        """Convert audio to text using Google Cloud Speech-to-Text.

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
            return self._transcribe_audio_binary(audio_binary_data)

        # if audio source is base64 encoded string
        if audio_binary_data := get_audio_from_base64(audio_source):
            self.logger.debug("Audio source is a valid base64 encoded audio string: %s", audio_source)
            return self._transcribe_audio_binary(audio_binary_data)

        # if audio source is downloadable audio URL
        if audio_binary_data := get_audio_from_downloadable_url(audio_source):
            self.logger.debug("Audio source is a valid downloadable audio URL: %s", audio_source)
            return self._transcribe_audio_binary(audio_binary_data)

        # if audio source is youtube URL
        if audio_binary_data := get_audio_from_youtube_url(audio_source, self.proxy):
            self.logger.debug("Audio source is a valid YouTube URL: %s", audio_source)
            return self._transcribe_audio_binary(audio_binary_data)

        raise ValueError("Unsupported audio source")

    def _transcribe_audio_binary(self, audio_binary_data: bytes) -> list[AudioTranscript]:
        """Transcribe audio binary data using Google Cloud Speech-to-Text.

        This method transcribe the audio binary using the Google Cloud Speech-to-Text API and returns the
        transcription results as a list of AudioTranscript.

        Args:
            audio_binary_data (bytes): Audio data in binary format.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects containing the transcribed audio.
        """
        # Google Cloud Speech-to-Text requires the following audio configuration:
        # 1. encoding: The audio encoding format (e.g. FLAC, LINEAR16)
        # 2. sample_rate_hertz: The sample rate of the audio in Hz
        # 3. audio_channel_count: Number of audio channels (mono=1, stereo=2)
        # those attributes are depend on the audio file format and the audio channel count
        # so we convert all input audio to a standardized mono FLAC format
        flac_binary_data = convert_audio_to_mono_flac(audio_binary_data)

        is_exceed_max_duration = get_audio_duration(flac_binary_data) > MAX_AUDIO_DURATION
        # For audio longer than 60 seconds, need to use URI instead of content
        if is_exceed_max_duration:
            self.logger.debug("Audio duration exceeds %d seconds, uploading to GCS", MAX_AUDIO_DURATION)
            destination_blob_name = self._upload_audio_to_gcs(flac_binary_data)
            audio = RecognitionAudio(uri=f"gs://{self.bucket_name}/{destination_blob_name}")
        else:
            audio = RecognitionAudio(content=flac_binary_data)

        config = RecognitionConfig(
            enable_automatic_punctuation=True,
            language_code=self.language_code,
            alternative_language_codes=self.alternative_language_codes,
            model=self.model,
            audio_channel_count=1,
        )

        self.logger.debug("Transcribing audio with config: %s", config)

        try:
            operation = self.speech_client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=self.timeout)
        except Exception as e:
            self.logger.error("Error transcribing audio: %s", e)
            raise e

        self.logger.debug("Received transcription response with %d results", len(response.results))

        if is_exceed_max_duration:  # Clean up the uploaded audio file
            self._delete_file_from_gcs(destination_blob_name)

        return self._convert_google_cloud_response_to_audio_transcripts(response)

    def _upload_audio_to_gcs(self, audio_binary_data: bytes) -> str:
        """Upload audio binary data to Google Cloud Storage.

        Args:
            audio_binary_data (bytes): Audio data in binary format.

        Returns:
            str: Destination blob name.
        """
        bucket = self.storage_client.bucket(self.bucket_name)

        destination_blob_name = f"audio-files/{uuid.uuid4()}.flac"
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(audio_binary_data)

        self.logger.debug("Successfully uploaded audio to GCS: %s", destination_blob_name)
        return destination_blob_name

    def _delete_file_from_gcs(self, destination_blob_name: str):
        """Delete file from Google Cloud Storage.

        Args:
            destination_blob_name (str): Destination blob name.
        """
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.delete()

        self.logger.debug("Successfully deleted audio file from GCS: %s", destination_blob_name)

    def _convert_google_cloud_response_to_audio_transcripts(self, response: RecognizeResponse) -> list[AudioTranscript]:
        """Convert the Google Cloud Speech-to-Text response to a list of AudioTranscript.

        This method processes the Google Cloud Speech-to-Text response and returns a list of AudioTranscript
        objects. Each transcript contains the recognized text, timing information, and language.

        Args:
            response (RecognizeResponse): The response from Google Cloud Speech-to-Text API containing
                recognition results.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects, each containing the transcribed text,
                start_time, end_time, and lang_id.
        """
        audio_transcripts = []

        for index, result in enumerate(response.results):
            start_time = 0 if index == 0 else response.results[index - 1].result_end_time.seconds
            end_time = result.result_end_time.seconds

            lang_id = self._convert_language_code_to_iso_639(result.language_code)

            # Get the most likely transcription
            transcript = result.alternatives[0].transcript

            # Create AudioTranscript object
            audio_transcript = AudioTranscript(
                text=transcript, start_time=start_time, end_time=end_time, lang_id=lang_id
            )
            audio_transcripts.append(audio_transcript)

        return audio_transcripts

    def _convert_language_code_to_iso_639(self, language_code: str) -> str | None:
        """Convert the language code to the ISO 639 code.

        Args:
            language_code (str): The language code to convert.

        Returns:
            str | None: The ISO 639 code. If the language code is not found, return None.
        """
        try:
            return Language.get(language_code).language
        except LanguageTagError:
            self.logger.debug("Failed to convert language code: %s to ISO 639 code", language_code)
            return None

"""Defines a module to convert audio to text using Prosa STT.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    [1] https://docs.google.com/document/d/1oTgi0f3ijgwvIdhfo5C7CrlA0ex44Y3UTtfDGnEOynk/edit?usp=sharing
    [2] https://docs2.prosa.ai/speech/stt/rest/getting_started/

Todo:
    - Standardize output format to use TextResult from gllm_multimodal.modality_converter.schema.text_result.py.
"""

import asyncio
import base64
import http
from urllib.parse import urlparse

import aiohttp
from gllm_core.utils.logger_manager import LoggerManager

from gllm_multimodal.modality_converter.audio_to_text.audio_to_text import BaseAudioToText
from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript
from gllm_multimodal.utils.audio_to_text_utils import (
    get_audio_duration,
    get_audio_from_base64,
    get_audio_from_file_path,
)

MAX_BASE64_AUDIO_DURATION = 55  # Limit set to 55s as 59s audio has hit Prosa STT's 60s max duration
MIN_POLLING_INTERVAL = 5


class ProsaAudioToText(BaseAudioToText):
    """An audio to text converter using Prosa STT.

    The ProsaAudioToText class is responsible for converting audio to text using the Prosa STT API.
    It supports various audio input formats and can handle audio from local files, base64 encoded strings,
    or URLs pointing to audio files.

    Attributes:
        url (str): The URL of the Prosa STT API.
        api_key (str): The API key for authenticating with the Prosa STT API.
        model (str): The model to use for the transcription.
        polling_interval (int): The interval between polling requests to the Prosa STT API.
    """

    def __init__(
        self,
        api_key: str,
        url: str = "https://api.prosa.ai/v2/speech/stt",
        model: str = "stt-general",
        polling_interval: int = MIN_POLLING_INTERVAL,
    ):
        """Initializes a new instance of the ProsaAudioToText class.

        Args:
            api_key (str): The API key for the Prosa STT API.
            url (str, optional): The URL of the Prosa STT API. Defaults to "https://api.prosa.ai/v2/speech/stt".
            model (str, optional): The model to use for the transcription. Defaults to "stt-general".
            polling_interval (int, optional): The interval between polling requests to the Prosa STT API.
                Defaults to MIN_POLLING_INTERVAL, which is set to 5 seconds.
        """
        self.api_key = api_key
        self.url = url
        self.model = model
        self._polling_interval = polling_interval
        self.logger = LoggerManager().get_logger(self.__class__.__name__)

    @property
    def polling_interval(self) -> int:
        """Get the polling interval in seconds.

        Returns:
            int: The current polling interval.
        """
        return self._polling_interval

    @polling_interval.setter
    def polling_interval(self, polling_interval: int):
        """Set the polling interval in seconds.

        Args:
            polling_interval (int): The new polling interval.

        Raises:
            ValueError: If the polling interval is not an int or is less than 5.
        """
        if not isinstance(polling_interval, int) or polling_interval < MIN_POLLING_INTERVAL:
            raise ValueError(f"Polling interval must be an int with minimum value of {MIN_POLLING_INTERVAL}")
        self._polling_interval = polling_interval

    async def convert(self, audio_source: str) -> list[AudioTranscript]:
        """Convert audio to text using the Prosa STT API.

        This method processes the given audio source and returns the transcribed text.
        The audio source can be a local file path, a base64 encoded string, or a URL.

        Args:
            audio_source (str): The source of the audio to be transcribed. Can be:
                - A path to a local audio file with maximum duration of 55 seconds.
                - A base64 encoded string of audio data with maximum duration of 55 seconds.
                - A direct HTTP/HTTPS URL that returns an audio file:
                    * Google Drive shared file URLs (e.g. https://drive.google.com/file/d/...)
                    * OneDrive shared file URLs (e.g. https://onedrive.live.com/...)
                    * S3 URLs (e.g. https://s3.amazonaws.com/...)
                    * Other HTTP URLs that directly serve audio files

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects containing the transcribed text.

        Raises:
            ValueError:
                - If the audio source is file path but the audio duration exceeds 55 seconds.
                - If the audio source is base64 encoded string but the audio duration exceeds 55 seconds.
                - If the audio source is not supported.
        """
        self.logger.debug("Converting audio source: %s", audio_source)

        # if audio source is a audio file path
        if audio_binary_data := get_audio_from_file_path(audio_source):
            self.logger.debug("Audio source is a valid audio file path: %s", audio_source)
            if get_audio_duration(audio_binary_data) <= MAX_BASE64_AUDIO_DURATION:
                audio_base64 = base64.b64encode(audio_binary_data).decode("utf-8")
                return await self._process_audio_transcription(audio_base64=audio_base64)
            raise ValueError("Audio duration exceeds 55 seconds (max duration for base64 encoding)")

        # if audio source is a audio in base64 encoded string
        if audio_binary_data := get_audio_from_base64(audio_source):
            self.logger.debug("Audio source is a valid base64 encoded audio string: %s", audio_source)
            if get_audio_duration(audio_binary_data) <= MAX_BASE64_AUDIO_DURATION:
                return await self._process_audio_transcription(audio_base64=audio_source)
            raise ValueError("Audio duration exceeds 55 seconds (max duration for base64 encoding)")

        # if audio source is a audio in URL
        if self._is_valid_url(audio_source):
            self.logger.debug("Audio source is a URL: %s", audio_source)
            return await self._process_audio_transcription(audio_url=audio_source)

        raise ValueError("Unsupported audio source")

    async def _process_audio_transcription(
        self, audio_base64: str = None, audio_url: str = None
    ) -> list[AudioTranscript]:
        """Process audio transcription using the Prosa STT API.

        This function handles the transcription process for either a base64 encoded audio or an audio URL.
        The user should provide either audio_base64 or audio_url. If both are provided, audio_base64
        will be used and audio_url will be ignored.

        Args:
            audio_base64 (str, optional): The base64 encoded audio data to be transcribed. Defaults to None.
            audio_url (str, optional): The URL of the audio file to be transcribed. Defaults to None.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects.

        Raises:
            ValueError: If neither audio_base64 nor audio_url is provided.
            ValueError: If the job ID is not found in the transcription request response.
        """
        if not audio_base64 and not audio_url:
            raise ValueError("Either audio_base64 or audio_url must be provided")

        self.logger.debug("Submitting transcription request: %s", audio_base64 if audio_base64 else audio_url)
        job = await self._submit_stt_request(audio_base64, audio_url)
        self.logger.debug("Received transcription request response: %s", job)

        job_id = job.get("job_id", None)

        if not job_id:
            raise ValueError(f"Failed to get job ID from transcription request. API response: {job}")

        while True:
            self.logger.debug("Polling transcription result for job ID: %s", job_id)
            result = await self._query_stt_result(job_id)
            if result is not None:
                self.logger.debug("Received transcription result: %s", result)
                break
            await asyncio.sleep(self.polling_interval)

        return self._result_to_audio_transcript(result)

    def _result_to_audio_transcript(self, result: dict) -> list[AudioTranscript]:
        """Convert the Prosa STT API result to a list of AudioTranscript objects.

        This method processes the raw result from the Prosa STT API, filters out unwanted data,
        sorts the transcripts by start time, and creates AudioTranscript objects for each valid transcript.

        Args:
            result (dict): The raw result from the Prosa STT API.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects representing the parsed and processed transcripts.
        """
        data = result.get("result", {}).get("data", [])

        # Sort and filter Prosa STT result data:
        # step 1: the output result from Prosa STT is not sorted by channel nor time_start
        sorted_data = sorted(data, key=lambda x: (x.get("channel", -1), x.get("time_start", 0)))

        # step 2: The result text from audio could have multiple channels
        #    1. The text from each channel could be the same or different
        #    2. If the text is the same, we only need to keep the Transcript from one channel
        #    3. If the text is different, we will keep the Transcript from all unique channels
        combined_text_by_channel = {}
        for item in sorted_data:
            channel = item.get("channel", -1)
            transcript = item.get("transcript", "")

            if channel not in combined_text_by_channel:
                combined_text_by_channel[channel] = transcript
            else:
                combined_text_by_channel[channel] += " " + transcript

        # get channel with unique combined text
        unique_channels = []
        current_unique_combined_texts = []
        for channel, text in combined_text_by_channel.items():
            if text not in current_unique_combined_texts:
                current_unique_combined_texts.append(text)
                unique_channels.append(channel)

        return [
            AudioTranscript(
                text=item.get("transcript", ""),
                start_time=item.get("time_start", 0),
                end_time=item.get("time_end", 0),
                lang_id=None,
            )
            for item in sorted_data
            if item.get("channel", -1) in unique_channels
        ]

    async def _query_stt_result(self, job_id: str) -> dict | None:
        """Query the Prosa STT API for the result of a transcription job.

        This method sends a GET request to the Prosa STT API to retrieve the result
        of a previously submitted transcription job.

        Args:
            job_id (str): The unique identifier of the transcription job.

        Returns:
            dict | None: The response from the Prosa STT API if the job is complete,
                or None if the job is still in progress or an error occurred.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.url}/{job_id}", headers={"x-api-key": self.api_key}, timeout=1 * 60
            ) as response:
                if response.status == http.HTTPStatus.OK:
                    result = await response.json()
                    if result["status"] == "complete":
                        return result

        return None

    async def _submit_stt_request(self, audio_base64: str = None, audio_url: str = None) -> dict:
        """Submit a request to the Prosa STT API for transcription.

        This method sends a POST request to the Prosa STT API to initiate a transcription job
        for the provided audio data. The audio data can be either base64 encoded or a URL.
        If both are provided, the base64 encoded audio will be used.

        Args:
            audio_base64 (str, optional): The base64 encoded audio data to be transcribed. Defaults to None.
            audio_url (str, optional): The URL of the audio file to be transcribed. Defaults to None.

        Returns:
            dict: The response from the Prosa STT API, typically containing a job ID
                  and other relevant information about the submitted transcription request.

        Raises:
            ValueError: If neither audio_base64 nor audio_url is provided.
        """
        if not audio_base64 and not audio_url:
            raise ValueError("Either audio_base64 or audio_url must be provided")

        request = {"data": audio_base64} if audio_base64 else {"uri": audio_url}

        payload = {
            "config": {
                "model": self.model,
                "wait": False,  # Do not wait for the request to complete
                "auto_punctuation": True,
            },
            "request": request,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url,
                json=payload,
                headers={"x-api-key": self.api_key},
                timeout=1 * 60,
            ) as response:
                return await response.json()

    def _is_valid_url(self, audio_source: str) -> bool:
        """Check if the audio source is a valid URL.

        Args:
            audio_source (str): The audio source to check.

        Returns:
            bool: True if the audio source is a valid URL, False otherwise.
        """
        result = urlparse(audio_source)
        return result.scheme == "https" and result.netloc

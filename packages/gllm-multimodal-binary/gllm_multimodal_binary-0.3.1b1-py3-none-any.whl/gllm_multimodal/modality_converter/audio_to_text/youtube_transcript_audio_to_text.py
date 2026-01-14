"""Defines a class for converting audio from YouTube to text using YouTube Transcript API.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    None

Todo:
    - Standardize output format to use TextResult from gllm_multimodal.modality_converter.schema.text_result.py.
"""

import re

import yt_dlp
from gllm_core.utils.logger_manager import LoggerManager
from youtube_transcript_api import CouldNotRetrieveTranscript, YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

from gllm_multimodal.modality_converter.audio_to_text.audio_to_text import BaseAudioToText
from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript


class YouTubeTranscriptAudioToText(BaseAudioToText):
    """An audio to text converter using YouTube Transcript API.

    The YoutubeTranscriptAudioToText class is responsible for converting audio from YouTube to text using
    YouTube Transcript API.

    Attributes:
        preferred_lang_ids (list[str]): The preferred language IDs for the transcript.
        allow_non_preferred_lang_ids (bool): Whether to allow non-preferred language IDs.
        allow_auto_generated_transcripts (bool): Whether to allow auto-generated transcripts.
        proxy (str | None): The proxy URL to use for the YouTube request.
    """

    def __init__(
        self,
        preferred_lang_ids: list[str] | None = None,
        allow_non_preferred_lang_ids: bool = False,
        allow_auto_generated_transcripts: bool = False,
        proxy: str | None = None,
    ):
        """Initialize the YouTubeTranscriptAudioToText instance.

        Args:
            preferred_lang_ids (list[str] | None, optional): The preferred language IDs for the transcript.
                Defaults to None, in which case ["id", "en"] will be used.
            allow_non_preferred_lang_ids (bool, optional): Whether to allow non-preferred language IDs.
                Defaults to False.
            allow_auto_generated_transcripts (bool, optional): Whether to allow auto-generated transcripts.
                Defaults to False.
            proxy (str | None, optional): The proxy URL to use for the YouTube request. Defaults to None.
        """
        self.preferred_lang_ids = preferred_lang_ids or ["id", "en"]
        self.allow_non_preferred_lang_ids = allow_non_preferred_lang_ids
        self.allow_auto_generated_transcripts = allow_auto_generated_transcripts
        self.proxy = proxy

        self.youtube_transcript_api = YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(https_url=proxy) if proxy else None
        )

        self.logger = LoggerManager().get_logger(self.__class__.__name__)

    async def convert(self, audio_source: str) -> list[AudioTranscript]:
        """Convert YouTube audio to text using the YouTube Transcript API.

        This method takes a YouTube URL as the audio source and retrieves the transcript
        using the YouTube Transcript API. It returns the transcript as a list of AudioTranscript.

        Args:
            audio_source (str): The YouTube URL of the audio source.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript.
        """
        self.logger.debug("Converting YouTube URL: %s", audio_source)

        video_id = self._extract_video_id(audio_source)
        self.logger.debug("Extracted video ID: %s", video_id)

        lang_id = self._select_best_transcript_lang_id(video_id)
        self.logger.debug("Selected language ID: %s", lang_id)

        return self._get_transcript(video_id, lang_id)

    def _get_transcript(self, video_id: str, lang_id: str) -> list[AudioTranscript]:
        """Retrieve the transcript for a given YouTube video and language ID.

        This method uses the YouTube Transcript API to fetch the transcript for the specified
        video ID and language ID. It processes the retrieved transcript data and converts it
        into a list of AudioTranscript objects.

        Args:
            video_id (str): The YouTube video ID.
            lang_id (str): The language ID for the transcript.

        Returns:
            list[AudioTranscript]: A list of AudioTranscript objects containing the transcribed text,
                start time, end time, and language ID.

        Raises:
            ValueError: If the transcript retrieval fails.
        """
        self.logger.debug("Getting transcript for video ID: %s, language ID: %s", video_id, lang_id)

        try:
            fetched_transcript = self.youtube_transcript_api.fetch(video_id, languages=[lang_id])
        except CouldNotRetrieveTranscript as e:
            raise ValueError(
                f"Failed to fetch transcript - Video ID: {video_id}, Language: {lang_id}, with error: {e}"
            ) from e

        self.logger.debug("Successfully fetched transcript with %d snippets", len(fetched_transcript.snippets))

        return [
            AudioTranscript(
                text=snippet.text,
                start_time=snippet.start,
                end_time=(snippet.start + snippet.duration),
                lang_id=lang_id,
            )
            for snippet in fetched_transcript.snippets
        ]

    def _select_best_transcript_lang_id(self, video_id: str) -> str:
        """Selects the best transcript language ID for a given YouTube video.

        This method attempts to find the best matching language code for the transcript of a YouTube
        video based on the user's preferences. The selection process follows this priority order:
        1. Language codes from manual transcripts in preferred languages
        2. Language codes from manual transcripts in non-preferred languages (if allowed)
        3. Language codes from auto-generated transcripts in preferred languages (if allowed)
        4. Language codes from auto-generated transcripts in non-preferred languages (if both auto-generated
           and non-preferred are allowed)

        Args:
            video_id (str): The YouTube video ID to get transcripts for.

        Returns:
            str: The selected language code for the transcript that best matches the
                configured preferences.

        Raises:
            ValueError:
                - If list of available transcripts retrieval fails.
                - If no suitable transcript is found based on the configured preferences.
        """
        try:
            transcripts = self.youtube_transcript_api.list(video_id)
        except CouldNotRetrieveTranscript as e:
            raise ValueError(f"Failed to fetch available transcripts - Video ID: {video_id}, Error: {e}") from e

        manual_lang_ids = [t.language_code for t in transcripts if not t.is_generated]
        self.logger.debug("Available manual language IDs: %s", manual_lang_ids)

        generated_lang_ids = [t.language_code for t in transcripts if t.is_generated]
        self.logger.debug("Available auto generated language IDs: %s", generated_lang_ids)

        for lang_id in self.preferred_lang_ids:
            if lang_id in manual_lang_ids:
                return lang_id

        if self.allow_non_preferred_lang_ids and manual_lang_ids:
            return manual_lang_ids[0]

        if self.allow_auto_generated_transcripts:
            for lang_id in self.preferred_lang_ids:
                if lang_id in generated_lang_ids:
                    return lang_id

            if self.allow_non_preferred_lang_ids and generated_lang_ids:
                return generated_lang_ids[0]

        raise ValueError(
            "No suitable transcript found - either no transcripts are available in preferred languages, "
            "or auto-generated/non-preferred language transcripts are disabled in settings"
        )

    def _extract_video_id(self, audio_source: str) -> str:
        """Extract the YouTube video ID from the audio source URL.

        Args:
            audio_source (str): The YouTube URL of the audio source.

        Returns:
            str: The YouTube video ID.

        Raises:
            ValueError: If video ID is not found from the provided YouTube URL.
        """
        proxy_opts = {"proxy": self.proxy} if self.proxy else {}
        ydl_opts = {"noplaylist": True, "quiet": True, **proxy_opts}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(audio_source, download=False)
                return info["id"]
        except yt_dlp.utils.DownloadError as e:
            error_message = str(e)
            self.logger.debug("yt-dlp failed to extract video ID, trying regex fallback. Error: %s", error_message)

        # fallback: Try regex patterns for various YouTube URL formats
        patterns = [
            r"(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|e\/|shorts\/)|youtu\.be\/)([\w-]{11})",
            r"youtube\.com\/.*[?&]v=([\w-]{11})",
            r"youtu\.be\/([\w-]{11})",
        ]

        for pattern in patterns:
            match = re.search(pattern, audio_source)
            if match:
                return match.group(1)

        raise ValueError(
            f"Unable to identify video ID from the provided YouTube URL: {audio_source}. yt-dlp error: {error_message}"
        )

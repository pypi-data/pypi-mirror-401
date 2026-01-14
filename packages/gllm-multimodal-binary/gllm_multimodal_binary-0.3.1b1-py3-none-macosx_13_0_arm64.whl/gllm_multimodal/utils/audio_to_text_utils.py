"""Utility functions for the audio to text process.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    None
"""

import base64
import http
import os
import re
from io import BytesIO

import numpy as np
import requests
import soundfile as sf
import yt_dlp
from gllm_core.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


def is_binary_data_audio(audio_binary_data: bytes) -> bool:
    """Check if the binary data is a valid audio file.

    Args:
        audio_binary_data (bytes): The binary data to check.

    Returns:
        bool: True if the binary data is a valid audio file, False otherwise.
    """
    try:
        sf.read(BytesIO(audio_binary_data))
        return True
    except Exception as e:
        logger.debug("The provided binary data is not a valid audio file with error: %s", e)
        return False


def get_audio_from_base64(audio_source: str) -> bytes | None:
    """Attempt to decode a base64 encoded audio string and verify if it's valid audio data.

    Args:
        audio_source (str): The potential base64 encoded audio string to decode.

    Returns:
        bytes | None: The decoded audio data if successful and valid, None otherwise.
    """
    try:
        logger.debug("Attempting to decode base64 encoded audio string: %s", audio_source)
        binary_data = base64.b64decode(audio_source, validate=True)
        return binary_data if is_binary_data_audio(binary_data) else None
    except Exception as e:
        logger.debug("The provided audio source is not a valid base64 encoded audio string with error: %s", e)
        return None


def get_audio_from_file_path(audio_source: str) -> bytes | None:
    """Read audio file and return its binary data if valid.

    Args:
        audio_source (str): Path to the audio file.

    Returns:
        bytes | None: Binary data of the audio file if valid, None otherwise.
    """
    try:
        logger.debug("Attempting to read audio file from file path: %s", audio_source)
        with open(audio_source, "rb") as file:
            audio_data = file.read()
            return audio_data if is_binary_data_audio(audio_data) else None
    except Exception as e:
        logger.debug("The provided audio source is not a valid audio file path with error: %s", e)
        return None


def get_audio_from_downloadable_url(audio_source: str, timeout: int = 1 * 60) -> bytes | None:
    """Get the audio from a downloadable URL and return its binary data if valid.

    This function attempts to download audio content from a downloadable URL (e.g. Google Drive, OneDrive)
    and validates that the downloaded content is audio data.

    Args:
        audio_source (str): The downloadable URL of the audio file.
        timeout (int): The timeout for the HTTP request in seconds. Defaults to 1 minute.

    Returns:
        bytes | None: Binary data of the audio file if valid audio content is downloaded,
            None if the request fails or content is not valid audio.
    """
    try:
        logger.debug("Attempting to download audio from downloadable URL: %s", audio_source)
        response = requests.get(audio_source, timeout=timeout)
    except Exception as e:
        logger.debug("The provided audio source is not a valid downloadable URL with error: %s", e)
        return None

    if response.status_code == http.HTTPStatus.OK:
        response_content = response.content
        return response_content if is_binary_data_audio(response_content) else None

    logger.debug("Failed to download audio with response status code: %s", response.status_code)
    return None


def get_audio_from_youtube_url(audio_source: str, proxy: str | None = None) -> bytes | None:
    """Extract audio from a YouTube video URL and return it as binary data.

    This function downloads a YouTube video and extracts its audio track in M4A format.
    The audio is stored in memory and validated before being returned.

    Args:
        audio_source (str): The YouTube video URL to extract audio from.
        proxy (str | None, optional): The proxy URL to use for the YouTube request. Defaults to None.

    Returns:
        bytes | None: Binary audio data if successfully downloaded and valid,
            None if download fails or audio is invalid.
    """
    save_dir = os.path.dirname(os.path.realpath(__file__))

    # Configure yt-dlp download options
    proxy_opts = {"proxy": proxy} if proxy else {}
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "noplaylist": True,
        "outtmpl": os.path.join(save_dir, "%(id)s.%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a"}],
        "quiet": True,
        **proxy_opts,
    }

    try:
        logger.debug("Attempting to extract audio from YouTube URL: %s", audio_source)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(audio_source, download=True)

        video_id = result.get("id", "")
        extension = result.get("ext", "m4a")

        if not video_id:
            logger.debug("Failed to get video ID from YouTube URL: %s", audio_source)
            return None

        file_name = f"{video_id}.{extension}"
        file_path = os.path.join(save_dir, file_name)
        audio_binary_data = get_audio_from_file_path(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

        return audio_binary_data

    except Exception as e:
        logger.debug("The provided audio source is not a valid YouTube URL with error: %s", e)
        return None


def get_audio_duration(audio_binary_data: bytes) -> float:
    """Get the duration of the audio in seconds.

    Args:
        audio_binary_data (bytes): The binary data of the audio.

    Returns:
        float: The duration of the audio in seconds.
    """
    with sf.SoundFile(BytesIO(audio_binary_data)) as audio:
        return len(audio) / audio.samplerate


def convert_audio_to_mono_flac(input_audio_bytes: bytes) -> bytes:
    """Convert audio binary data to mono FLAC format.

    This method standardizes the audio format to mono FLAC to simplify processing by having a consistent
    file extension and single audio channel, while preserving the audio information.

    This method performs two operations:
    1. Converts the input audio to mono (single channel)
    2. Encodes the audio in FLAC format for optimal speech recognition

    FLAC (Free Lossless Audio Codec) is chosen because:
    1. Lossless compression preserves audio quality for accurate transcription
    2. More bandwidth efficient compared to uncompressed formats like LINEAR16
    3. supports variable bit depths (16/24-bit) automatically -> no need to specify sample rate

    Mono channel is chosen because:
    1. Speech recognition models are optimized for single-channel audio
    2. Reduces bandwidth and processing overhead
    3. Simplifies processing by avoiding multi-channel complexity
    4. Ensures consistent results across different input formats

    Args:
        input_audio_bytes (bytes): Input audio data in binary format.

    Returns:
        bytes: Audio data converted to mono FLAC format.
    """
    logger.debug("Converting audio to mono FLAC format")

    # Load audio from bytes into a soundfile
    with sf.SoundFile(BytesIO(input_audio_bytes)) as audio:
        data = audio.read()
        samplerate = audio.samplerate

    # Convert to mono by averaging channels if stereo
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Create an in-memory buffer for FLAC encoding
    flac_buffer = BytesIO()

    # Export as FLAC with optimal speech recognition settings
    sf.write(flac_buffer, data, samplerate, format="FLAC", subtype="PCM_24")
    flac_audio_binary_data = flac_buffer.getvalue()

    logger.debug("Successfully converted audio to mono FLAC format")
    return flac_audio_binary_data


def detect_audio_format(audio_binary_data: bytes) -> str | None:
    """Detect the audio format from binary data.

    This function attempts to identify the audio format by reading the audio file metadata.
    The format detection is performed using the soundfile library, which can identify common
    audio formats like MP3, WAV, FLAC, OGG, etc.

    Args:
        audio_binary_data (bytes): The binary data of the audio.

    Returns:
        str | None: The detected audio format in lowercase (e.g., 'mp3', 'wav', 'flac'), or None if detection fails.
    """
    try:
        with sf.SoundFile(BytesIO(audio_binary_data)) as audio:
            if hasattr(audio, "format"):
                detected_format = audio.format.lower()
                logger.debug("Detected audio format: %s", detected_format)
                return detected_format
            logger.debug("Audio format attribute not found")
            return None
    except Exception as e:
        logger.debug("Failed to detect audio format with error: %s", e)
        return None


def is_youtube_url(source: str) -> bool:
    """Check if the audio source is a YouTube URL.

    Args:
        source (str): The audio source to check.

    Returns:
        bool: True if the audio source is a YouTube URL, False otherwise.
    """
    # Match youtube.com and youtu.be domains with various subdomains and protocols
    youtube_pattern = re.compile(r"^(https?://)?(www\.|m\.)?(youtube\.com|youtu\.be)(/.*)?$", re.IGNORECASE)
    return bool(youtube_pattern.match(source))

"""Video utilities for frame extraction and video processing.

This module provides utility functions for working with video files, including
frame extraction at specific timestamps.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

Reviewers:
    NONE
"""

import os
from io import BytesIO

from gllm_core.utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(__name__)


def extract_video_frame_at_timestamp(
    video_path: str,
    timestamp: float,
    output_format: str = "PNG",
) -> bytes:
    """Extract a single frame from a video at a specific timestamp.

    This function extracts a frame from a video file at the specified timestamp
    and returns it as raw image bytes in the specified format.

    Args:
        video_path (str): Path to the video file.
        timestamp (float): Time offset in seconds from which to extract the frame.
        output_format (str, optional): Image format for the output (PNG, JPEG, etc.).
            Defaults to "PNG".

    Returns:
        bytes: Raw image bytes in the specified format.

    Raises:
        FileNotFoundError: If the video file doesn't exist.
        ValueError: If timestamp is negative or frame extraction fails.
        ImportError: If required libraries (cv2/opencv-python) are not installed.

    Examples:
        >>> frame_bytes = extract_video_frame_at_timestamp("video.mp4", 5.5)
        >>> frame_bytes = extract_video_frame_at_timestamp("video.mp4", 10.0, "JPEG")
    """
    logger.debug(f"Extracting frame from {video_path} at timestamp {timestamp}s")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if timestamp < 0:
        raise ValueError(f"Timestamp must be non-negative, got: {timestamp}")

    try:
        import cv2
    except ImportError as e:
        raise ImportError(
            "opencv-python is required for video frame extraction. "
            "Install video dependencies with: pip install gllm-multimodal[video]"
        ) from e

    try:
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video file: {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            raise ValueError(f"Invalid FPS ({fps}) in video file: {video_path}")

        # Calculate frame number from timestamp
        frame_number = int(timestamp * fps)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if frame_number >= total_frames:
            logger.warning(
                f"Timestamp {timestamp}s (frame {frame_number}) exceeds video duration. "
                f"Using last frame (frame {total_frames - 1})."
            )
            frame_number = total_frames - 1

        # Seek to the specific frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise ValueError(f"Failed to extract frame at timestamp {timestamp}s from {video_path}")

        # Convert BGR (OpenCV format) to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image for format conversion
        try:
            from PIL import Image
        except ImportError as e:
            raise ImportError(
                "Pillow is required for image format conversion. "
                "Install video dependencies with: pip install gllm-multimodal[video]"
            ) from e

        pil_image = Image.fromarray(frame_rgb)

        # Convert to bytes
        buffer = BytesIO()
        pil_image.save(buffer, format=output_format)
        buffer.seek(0)
        image_bytes = buffer.read()

        logger.debug(f"Successfully extracted frame at {timestamp}s")

        return image_bytes

    except (cv2.error, Exception) as e:
        raise ValueError(f"Error extracting frame from video {video_path} at timestamp {timestamp}s: {e}") from e

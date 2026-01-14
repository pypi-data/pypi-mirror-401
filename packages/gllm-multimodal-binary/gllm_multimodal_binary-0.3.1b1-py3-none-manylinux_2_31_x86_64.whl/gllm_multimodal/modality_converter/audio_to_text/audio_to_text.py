"""Defines a base class for audio to text converter used in Gen AI applications.

Authors:
    Obryan Ramadhan (obryan.ramadhan@gdplabs.id)

References:
    NONE

TODO: change the base class from Component to BaseModalityConverter
"""

from abc import ABC, abstractmethod
from typing import Any

from gllm_core.schema import Component

from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript


class BaseAudioToText(Component, ABC):
    """An abstract base class for audio to text used in Gen AI applications.

    This class provides a foundation for building audio to text converter components in Gen AI applications.
    """

    async def _run(self, **kwargs: Any) -> list[AudioTranscript]:
        """Executes the audio to text process.

        This method calls `convert` to perform the audio to text process, passing along any provided arguments.

        Args:
            **kwargs (Any): A dictionary of arguments required for the audio to text process.
                Must include `audio_source` of type `str`.

        Returns:
            list[AudioTranscript]: A list of audio transcripts.

        Raises:
            ValueError: If `audio_source` is missing from the input kwargs or is not a non-empty string.
        """
        if (
            "audio_source" not in kwargs
            or not isinstance(kwargs["audio_source"], str)
            or not kwargs["audio_source"].strip()
        ):
            raise ValueError(
                "The input kwargs for audio to text must include a non-empty `audio_source` key of type `str`."
            )

        return await self.convert(kwargs["audio_source"])

    @abstractmethod
    async def convert(self, audio_source: str) -> list[AudioTranscript]:
        """Converts audio to text from a given source.

        This abstract method must be implemented by subclasses to define how the audio is converted to text.
        It is expected to return a list of audio transcripts.

        Args:
            audio_source (str): The source of the audio to be transcribed.

        Returns:
            list[AudioTranscript]: A list of audio transcripts.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement the `convert` method to define the audio to text conversion process."
        )

    def _format_input_event(self, input_dict: dict) -> str:
        """Formats an event message detailing the input data for the audio to text conversion process.

        This method constructs an event message that includes the class name and the input data.

        Args:
            input_dict (dict): A dictionary containing the input data, including the `audio_source` key.

        Returns:
            str: A formatted event message indicating the start of the audio to text conversion process.
        """
        message = (
            f"[Start {self.__class__.__name__!r}] Converting audio to text from: {input_dict.get('audio_source')!r}"
        )
        return message

    def _format_output_event(self, output: list[AudioTranscript]) -> str:
        """Formats an event message detailing the results of the audio to text conversion process.

        This method constructs an event message that includes the class name and the number of audio transcripts.

        Args:
            output (list[AudioTranscript]): A list of audio transcripts.

        Returns:
            str: A formatted event message indicating the completion of the audio to text
                conversion process and the results.
        """
        message = f"[Finished {self.__class__.__name__!r}] Converted audio to text: {len(output)} audio transcript(s)"
        return message

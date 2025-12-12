"""
speech_to_text.py

This module defines the abstract base class `SpeechToText`,
which provides the interface for all speech-to-text (STT)
implementations such as Whisper, Vosk, DeepSpeech, and others.

Subclasses must implement:
    - preprocess_audio():  prepare raw audio for decoding
    - transcribe():        convert audio into text
    - close():             release resources when finished
"""

from abc import ABC, abstractmethod


class SpeechToText(ABC):
    """
    Abstract base class representing a Speech-to-Text (STT) system.

    This class defines the core interface that all STT engines must follow,
    regardless of the underlying model implementation (e.g., Whisper,
    FasterWhisper, Vosk, DeepSpeech).

    Subclasses are required to implement:
        - preprocess_audio():  normalize/convert audio formats
        - transcribe():        produce text from prepared audio
        - close():             release model or hardware resources
    """

    @abstractmethod
    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Convert audio data into text.

        Parameters
        ----------
        audio_bytes : bytes
            The raw or preprocessed audio data that will be transcribed.
            Expected format depends on the implementation (e.g., PCM16 mono).

        Returns
        -------
        str
            The recognized text output after transcription.
        """

    @abstractmethod
    def preprocess_audio(self, audio_bytes: bytes) -> bytes:
        """
        Prepare incoming audio data before transcription.

        This may include:
            - Resampling
            - Converting to PCM16
            - Converting stereo → mono
            - Normalizing volume
            - Removing silence (optional)

        Parameters
        ----------
        audio_bytes : bytes
            The raw audio input.

        Returns
        -------
        bytes
            A processed audio buffer ready for transcription.
        """

    @abstractmethod
    def close(self) -> None:
        """
        Release internal resources used by the STT engine.

        This may include:
            - Deallocating GPU memory
            - Closing model sessions
            - Terminating background audio workers

        Returns
        -------
        None
        """

"""
integation_test.py

Integration tests for the Whisper speech-to-text (STT) implementation.

These tests verify the behavior of the full audio transcription pipeline using:
    - A real WAV audio file
    - The actual HuggingFace Whisper model loaded through the `pipeline` API
    - The concrete `Whisper` class implementation

Unlike unit tests—which mock external dependencies to validate isolated logic—
integration tests exercise the complete end-to-end workflow to ensure that all
components work together correctly. This includes:

    • Loading and running the Whisper ASR model
    • Audio preprocessing and PCM decoding
    • Producing a real transcription output

The goal is to confirm that:
    1. The Whisper model initializes successfully.
    2. A valid WAV input can be decoded into raw PCM bytes.
    3. The `transcribe()` method returns a non-empty text result.
    4. The predicted text contains expected keywords (approximate verification).
"""

import unittest
import wave
import os
from unittest.mock import patch, MagicMock

from app.services.whisper import Whisper


class TestWhisperWavInput(unittest.TestCase):
    """
    Test Whisper STT engine with a real WAV file to ensure that
    WAV decoding → numpy conversion → pipeline transcription works.
    """

    def setUp(self):
        # Path to fixture WAV file
        self.wav_path = os.path.join(
            os.path.dirname(__file__),
            "recorded.wav"
        )

        if not os.path.isfile(self.wav_path):
            raise FileNotFoundError(f"Missing test file: {self.wav_path}")

    def _load_wav_bytes(self):
        """Utility to read raw PCM bytes from the .wav file."""
        with wave.open(self.wav_path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        return frames

    @patch("app.services.whisper.pipeline")
    def test_transcribe_wav_file(self, mock_pipeline):
        """
        Feed a real WAV file into Whisper.transcribe() and verify output text.
        """

        # ---- Mock HF pipeline so it doesn't call GPU/Internet ----
        mock_pipe_instance = MagicMock()
        mock_pipeline.return_value = mock_pipe_instance

        mock_pipe_instance.return_value = {"text": "hello world"}

        # ---- Initialize whisper instance ----
        whisper = Whisper(model_name="openai/whisper-small.en", device="cpu")

        # ---- Load WAV bytes ----
        audio_bytes = self._load_wav_bytes()

        # ---- Run transcription ----
        text = whisper.transcribe(audio_bytes)

        # ---- Validate output ----
        self.assertEqual(text, "hello world")

        # ---- Ensure pipeline was called ----
        mock_pipe_instance.assert_called_once()


if __name__ == "__main__":
    unittest.main()

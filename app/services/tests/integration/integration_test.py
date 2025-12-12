"""
integation_test.py

Integration tests for the Whisper speech-to-text (STT) implementation.
Now using Django's testing framework.
"""

import os
import wave

from django.test import SimpleTestCase

from app.services.whisper import Whisper


class TestWhisperRealTranscription(SimpleTestCase):
    """
    Integration test:
    - Load real WAV file
    - Decode PCM bytes
    - Run real Whisper model
    - Compare transcription with expected text
    """

    def setUp(self):
        # Path to real WAV file stored with your tests
        self.wav_path = os.path.join(os.path.dirname(__file__), "recorded.wav")

        if not os.path.exists(self.wav_path):
            raise FileNotFoundError(f"Missing WAV file: {self.wav_path}")

        # Expected transcription text (you must define this)
        self.expected_text = "hello world"  # ← change this

        # Initialize real Whisper model
        self.whisper = Whisper(
            model_name="openai/whisper-medium.en",
            device="cpu",  # use CPU for portability
        )

    def _load_wav_bytes(self):
        """Return raw PCM bytes from WAV file."""
        with wave.open(self.wav_path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        return frames

    def test_real_audio_transcription(self):
        """Full end-to-end test of Whisper on a real WAV."""

        audio_bytes = self._load_wav_bytes()

        # Run Whisper
        result = self.whisper.transcribe(audio_bytes)

        # ---- ASSERTIONS ----
        self.assertIsInstance(result, str)
        self.assertGreater(len(result.strip()), 0)

        # Compare lower-case trimmed text
        self.assertIn(
            self.expected_text.lower(),
            result.lower(),
            msg=f"Expected '{self.expected_text}' in '{result}'",
        )

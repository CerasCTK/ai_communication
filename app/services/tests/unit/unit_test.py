"""
unit_test.py

Unit tests for verifying the SpeechToText abstract base class.
This test suite ensures that all required abstract methods
(`transcribe`, `preprocess_audio`, `close`) are defined on the
SpeechToText interface. It does not instantiate SpeechToText
directly because doing so is prohibited for abstract classes.
"""

import unittest
from unittest.mock import MagicMock, patch
from app.services.whisper import Whisper
from app.services.speech_to_text import SpeechToText


class TestSpeechToTextBase(unittest.TestCase):
    """
    Verify the abstract base class contract.
    """
    def test_abstract_methods_exist(self):
        """
        Test Abstact method exixts.
        """
        self.assertTrue(hasattr(SpeechToText, "transcribe"))
        self.assertTrue(hasattr(SpeechToText, "preprocess_audio"))
        self.assertTrue(hasattr(SpeechToText, "close"))


class TestWhisperSTT(unittest.TestCase):
    """Tests for the Whisper STT implementation."""

    @patch("app.services.whisper.pipeline")
    def test_transcribe_mock(self, mock_pipeline):
        """Test transcription with mocked Whisper pipeline."""

        # ---- Prepare fake pipeline result ----
        fake_pipe = MagicMock()
        fake_pipe.return_value = {"text": "hello world"}
        mock_pipeline.return_value = fake_pipe

        # ---- Prepare fake audio input ---
        fake_audio = b"\x00\x01" * 1000  # fake PCM16 bytes
        # ---- Create Whisper instance ----
        stt = Whisper(model_name="openai/whisper-small", device="cpu")

        # ---- Test preprocess_audio ----
        processed = stt.preprocess_audio(fake_audio)
        self.assertEqual(processed, fake_audio)

        # ---- Test transcribe() ----
        text = stt.transcribe(fake_audio)
        self.assertEqual(text, "hello world")

        # Ensure pipeline was called
        fake_pipe.assert_called()

    def test_close(self):
        """Ensure close() does not raise errors."""
        stt = Whisper(model_name="openai/whisper-small", device="cpu")

        try:
            stt.close()
        except RuntimeError as e:
            self.fail(f"close() raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()

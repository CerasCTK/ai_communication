"""
test_whisper_logic.py

Clean unit test: directly tests Whisper.transcribe()
without WAV file, without filesystem, no mocks.
"""

from django.test import SimpleTestCase

from app.services.whisper import Whisper


class TestWhisperLogic(SimpleTestCase):
    """
    Test the logical behavior of Whisper.transcribe()
    with simple fake audio bytes.
    """

    def setUp(self):
        # Initialize Whisper in CPU mode
        self.whisper = Whisper(model_name="openai/whisper-small.en", device="cpu")

    def test_transcribe_returns_string(self):
        """
        Ensure the function returns a string.
        """

        # Fake audio data (just bytes, not real audio)
        dummy_audio = b"\x00\x01\x02\x03\x04\x05"

        text = self.whisper.transcribe(dummy_audio)

        # Basic assertion: must return a string
        self.assertIsInstance(text, str)

    def test_transcribe_not_empty(self):
        """
        Ensure transcription output is not empty.
        """

        dummy_audio = b"\x10\x20\x30\x40"

        text = self.whisper.transcribe(dummy_audio)

        self.assertTrue(len(text.strip()) > 0)
        self.assertTrue(len(text.strip()) > 0)

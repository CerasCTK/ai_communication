"""
whisper.py

Concrete implementation of the SpeechToText abstract class using
Faster-Whisper, PyAudio, and WebRTC VAD for streaming transcription.
"""

from typing import Generator
from transformers import pipeline
import pyaudio
import webrtcvad
import requests
import numpy as np
from .speech_to_text import SpeechToText


DJANGO_API = "http://127.0.0.1:8000/receive_transcript/"
SAMPLE_RATE = 16000
CHUNK_DURATION = 0.512  # seconds
BUFFER_DURATION = 3  # seconds


class Whisper(SpeechToText):
    """
    Whisper STT engine using Faster-Whisper + VAD + PyAudio streaming.

    This class handles:
        - audio capture via PyAudio
        - VAD segmentation using WebRTC VAD
        - buffering logic for speech chunks
        - transcription using Faster-Whisper
        - sending transcriptions to Django server

    Implements required abstract methods:
        - preprocess_audio()
        - transcribe()
        - close()
    """

    def __init__(
        self,
        model_name: str = "openai/whisper-medium.en",
        device: str = "cuda",
    ):
        """Load HuggingFace Whisper pipeline and initialize components."""
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            device=0 if device == "cuda" else -1
        )

        self.vad = webrtcvad.Vad()
        self.vad.set_mode(2)

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=1024,
        )

        self.buffer_audio = b""
        self.accumulated_transcription = ""

    # ============================================================
    # Abstract method implementations
    # ============================================================

    def preprocess_audio(self, audio_bytes: bytes) -> bytes:
        """Return raw PCM16 mono audio (already PCM16)."""
        return audio_bytes

    def transcribe(self, audio_bytes) -> str:
        """Transcribe with pipeline."""
        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)/32768.0
        result = self.pipe(audio_np)
        return result["text"].strip()

    def close(self) -> None:
        """Release PyAudio streams and Whisper model."""
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
        except Exception:
            pass

    # ============================================================
    # Utility methods
    # ============================================================

    def _record_small_chunk(self) -> bytes:
        """Record a small chunk of raw PCM audio."""
        frames = []
        num_frames = int(SAMPLE_RATE * CHUNK_DURATION / 1024)
        for _ in range(num_frames):
            data = self.stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        return b"".join(frames)

    def _frame_generator(
        self,
        audio_bytes: bytes,
        frame_duration_ms: int = 30
    ) -> Generator[bytes, None, None]:
        """Generate frames of fixed duration for VAD."""
        bytes_per_frame = int(SAMPLE_RATE * 2 * frame_duration_ms / 1000)
        for i in range(0, len(audio_bytes), bytes_per_frame):
            frame = audio_bytes[i:i + bytes_per_frame]
            if len(frame) == bytes_per_frame:
                yield frame

    def _is_speech(
        self,
        audio_bytes: bytes
    ) -> bool:
        """Detect if chunk contains speech."""
        for frame in self._frame_generator(audio_bytes):
            if self.vad.is_speech(frame, SAMPLE_RATE):
                return True
        return False

    def _send_text(
        self,
        text: str
    ) -> None:
        """Send text transcript to Django."""
        try:
            requests.post(DJANGO_API, json={"text": text})
        except Exception as e:
            print("Send text error:", e)

    # ============================================================
    # Live streaming loop
    # ============================================================

    def start_streaming(self) -> None:
        """
        Start VAD-powered streaming transcription.
        This function blocks until KeyboardInterrupt.
        """
        print("Listening... Press Ctrl+C to stop.")

        try:
            while True:
                small_chunk = self._record_small_chunk()

                # Speech?
                if self._is_speech(small_chunk):
                    self.buffer_audio += small_chunk

                # Enough buffer?
                if len(self.buffer_audio) >= SAMPLE_RATE * 2 * BUFFER_DURATION:
                    transcription = self.transcribe(self.buffer_audio)
                    self.buffer_audio = b""

                    if transcription:
                        print("\033[92m" + transcription + "\033[0m")
                        self.accumulated_transcription += transcription + " "
                        # self._send_text(transcription)

        except KeyboardInterrupt:
            print("\n--- Transcription finished ---")
            print("Full transcript:\n", self.accumulated_transcription)
            self.close()

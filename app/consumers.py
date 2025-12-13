import numpy as np
import webrtcvad
from channels.generic.websocket import AsyncWebsocketConsumer
from app.services.whisper import Whisper

# Initialize Whisper once (shared across clients)
whisper = Whisper(model_name="medium.en", device="cuda")

SAMPLE_RATE = 16000
BUFFER_DURATION_SECS = 3  # accumulate 3 seconds of speech before transcribing
VAD_MODE = 2  # 0=least aggressive, 3=most aggressive
OVERLAP_SECS = 0.5  # keep last 0.5s to preserve short words
RMS_THRESHOLD = 500  # adjust based on microphone input


class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.audio_buffer = b""  # per-client buffer
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(VAD_MODE)
        print("Client connected")

    def _is_speech(self, audio_bytes: bytes) -> bool:
        """Return True if any 30ms frame contains speech above RMS threshold."""
        frame_duration_ms = 30
        bytes_per_frame = int(SAMPLE_RATE * 2 * frame_duration_ms / 1000)  # 16-bit PCM

        for i in range(0, len(audio_bytes), bytes_per_frame):
            frame = audio_bytes[i:i + bytes_per_frame]
            if len(frame) != bytes_per_frame:
                continue

            if self.vad.is_speech(frame, SAMPLE_RATE):
                # Compute RMS to filter very low-energy noise
                audio_np = np.frombuffer(frame, dtype=np.int16)
                rms = np.sqrt(np.mean(audio_np.astype(np.float32) ** 2))
                if rms > RMS_THRESHOLD:
                    return True
        return False

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Append only if chunk contains real speech
            if self._is_speech(bytes_data):
                self.audio_buffer += bytes_data

            # Transcribe if enough speech accumulated
            min_bytes = SAMPLE_RATE * 2 * BUFFER_DURATION_SECS
            if len(self.audio_buffer) >= min_bytes:
                pcm16 = np.frombuffer(self.audio_buffer, dtype=np.int16)
                text = whisper.transcribe(pcm16)

                if text.strip():
                    print("Transcribed:", text)
                    await self.send(text_data=text)

                # Keep last 0.5s for overlap to catch short words
                overlap_bytes = int(SAMPLE_RATE * 2 * OVERLAP_SECS)
                self.audio_buffer = self.audio_buffer[-overlap_bytes:]

    async def disconnect(self, code):
        print("Client disconnected")

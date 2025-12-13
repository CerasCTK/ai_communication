import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from app.services.whisper import Whisper

whisper = Whisper(model_name="medium.en", device="")

class AudioConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.audio_buffer = bytes()   # buffer riêng cho từng client
        print("Client connected")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.audio_buffer += bytes_data

            # mỗi 0.5s  = 16000Hz * 2 bytes * 0.5s = 16000 bytes
            if len(self.audio_buffer) >= 16000 * 2:
                pcm16 = np.frombuffer(self.audio_buffer, dtype=np.int16).astype(np.float32)
                pcm16 = pcm16 / 32768  # chuẩn hóa [-1;1]

                text = whisper.transcribe(pcm16)
                print("Transcribed:", text)

                await self.send(text_data=text)

                self.audio_buffer = bytes()  # flush

    async def disconnect(self, code):
        print("Client disconnected")

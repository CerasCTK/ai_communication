import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .openai_client import process_audio_with_openai

class AudioConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"status": "connected"}))

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            response_text = await process_audio_with_openai(bytes_data)

            await self.send(json.dumps({
                "result": response_text
            }))
        else:
            await self.send(json.dumps({"error": "No audio received"}))

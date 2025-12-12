"""
WebSocket consumer module for handling real-time audio communication.

This module defines the AudioConsumer class, which manages WebSocket events
such as connection establishment, receiving messages, and handling disconnections.
"""

from channels.generic.websocket import AsyncWebsocketConsumer
from app.services.whisper import Whisper

whisper = Whisper(model_name="medium.en", device="cuda")


class AudioConsumer(AsyncWebsocketConsumer):
    """
    Asynchronous WebSocket consumer for processing audio and text messages.

    This consumer:
    - Accepts incoming WebSocket connections.
    - Sends an initial confirmation message.
    - Echoes back received text or binary data.
    """

    async def connect(self) -> None:
        """
        Handle a new WebSocket connection request.

        Upon connection:
            - The connection is accepted.
            - A confirmation message is sent to the client.
        """
        await self.accept()
        print("Client connected")
        await self.send(text_data="Connected OK!")

    async def receive(
        self, text_data: str | None = None, bytes_data: bytes | None = None
    ) -> None:
        """
        Handle incoming WebSocket messages.

        """
        print("Haa")
        # Receive PCM bytes from client
        if bytes_data:
            # Call your transcribe() directly
        
            text = whisper.transcribe(bytes_data)
            print("Transcribed:", text)

            # Send back to browser
            await self.send(text_data=text)

    async def disconnect(self, code: int) -> None:
        """
        Handle WebSocket disconnection.

        """
        whisper.close()
        print("Client disconnected")

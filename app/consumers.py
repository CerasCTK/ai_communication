"""
WebSocket consumer module for handling real-time audio communication.

This module defines the AudioConsumer class, which manages WebSocket events
such as connection establishment, receiving messages, and handling disconnections.
"""

from channels.generic.websocket import AsyncWebsocketConsumer


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
        await self.send(text_data="Connected OK!")

    async def receive(
        self, text_data: str | None = None, bytes_data: bytes | None = None
    ) -> None:
        """
        Handle incoming WebSocket messages.

        Args:
            text_data (str | None): Text data sent by client (if any).
            bytes_data (bytes | None): Binary/audio data sent by client (if any).

        Behavior:
            - If text is received → send formatted echo response.
            - If binary data is received → return the same bytes.
        """
        if text_data is not None:
            await self.send(text_data=f"Echo: {text_data}")
        elif bytes_data is not None:
            await self.send(bytes_data=bytes_data)

    async def disconnect(self, code: int) -> None:
        """
        Handle WebSocket disconnection.

        Args:
            close_code (int): Code indicating why the connection was closed.

        This method is executed when:
            - Client disconnects.
            - Server terminates the WebSocket.
        """

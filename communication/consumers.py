# communication/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer


class AudioConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling audio streaming and basic echo messages.
    """

    async def connect(self) -> None:
        """Handle new websocket connection."""
        await self.accept()
        await self.send(text_data="Connected OK!")

    async def receive(
        self, text_data: str | None = None, bytes_data: bytes | None = None
    ) -> None:
        """Handle received text or binary data."""
        if text_data is not None:
            await self.send(text_data=f"Echo: {text_data}")
        elif bytes_data is not None:
            await self.send(bytes_data=bytes_data)

    # pylint: disable=arguments-renamed
    async def disconnect(self, close_code: int) -> None:
        """Handle websocket disconnection."""

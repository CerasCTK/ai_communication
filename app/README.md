📡 WebSocket Audio Consumer – Documentation
📝 Overview

This module provides a simple WebSocket service using Django Channels.
It supports:

Real-time WebSocket connection

Text message handling (echo server)

Binary data handling (audio bytes, files, streaming)

Basic connection lifecycle events

The consumer is located in:

communication/consumers.py

📁 Code: AudioConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class AudioConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling audio streaming and basic echo messages.
    """

    async def connect(self) -> None:
        """Handle new websocket connection."""
        await self.accept()
        await self.send(text_data="Connected OK!")

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        """Handle received text or binary data."""
        if text_data is not None:
            await self.send(text_data=f"Echo: {text_data}")
        elif bytes_data is not None:
            await self.send(bytes_data=bytes_data)

    async def disconnect(self, close_code: int) -> None:
        """Handle websocket disconnection."""
        pass

🔌 WebSocket Routing

File: communication/routing.py

from django.urls import path
from .consumers import AudioConsumer

websocket_urlpatterns = [
    path("ws/audio/", AudioConsumer.asgi()),
]

⚙️ ASGI Configuration

File: ai_communication/asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import communication.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_communication.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(communication.routing.websocket_urlpatterns)
    ),
})

▶️ How to Run
1. Install required packages
pip install channels channels_redis django


(Redis is optional unless you use channel layer.)

2. Start Django server
python manage.py runserver


WebSocket endpoint becomes available at:

ws://127.0.0.1:8000/ws/audio/

🧪 Testing the WebSocket
✔ Test in Browser Console

Open DevTools → Console:

let socket = new WebSocket("ws://127.0.0.1:8000/ws/audio/");

socket.onopen = () => {
    console.log("Connected!");
    socket.send("Hello server!");
};

socket.onmessage = event => {
    console.log("Server:", event.data);
};


Expected response:

Connected OK!
Echo: Hello server!

✔ Test with Python Client
import websockets
import asyncio

async def test():
    async with websockets.connect("ws://127.0.0.1:8000/ws/audio/") as ws:
        await ws.send("Hello!")
        print(await ws.recv())

asyncio.run(test())

✔ Test Sending Binary (audio bytes)
socket.send(new Blob([audioBuffer]));


Server will return the same bytes (echo).

🎧 Features Supported
Feature	Description
WebSocket connection	Accepts and confirms connection
Text messages	Echoes received string messages
Binary messages	Echoes audio data / bytes
Disconnect handling	Hook provided for cleanup (optional)
📌 Notes for Extension

You can expand this consumer to support:

Audio streaming between clients

Speech-to-text processing

Forwarding audio to AI models

Group channels (broadcast)

Saving audio to storage

📦 Summary

This WebSocket consumer serves as a foundation for real-time audio or messaging features.
It is simple, lightweight, and easy to extend for AI, voice chat, or streaming applications.
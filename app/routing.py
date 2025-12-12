"""
WebSocket URL routing for the 'app' Django application.

This module maps WebSocket endpoints to their corresponding consumer classes.
It is imported by the project's ASGI configuration to register WebSocket routes.
"""

from django.urls import re_path

from .consumers import AudioConsumer

# WebSocket endpoint definitions for the app.
# Each path maps to an AsyncWebsocketConsumer subclass.
websocket_urlpatterns = [
    re_path(r"^ws/audio/$", AudioConsumer.as_asgi()),
]

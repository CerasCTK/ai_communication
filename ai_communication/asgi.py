"""
ASGI configuration for the ai_communication project.

This file integrates Django's ASGI application with Django Channels,
enabling support for both HTTP and WebSocket protocols.
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import app.routing  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_communication.settings")

# Standard Django ASGI application (handles HTTP requests)
django_asgi_app = get_asgi_application()

# Top-level ASGI application
application = ProtocolTypeRouter(
    {
        # Handles traditional HTTP requests
        "http": django_asgi_app,
        # Handles WebSocket protocol using Django Channels
        "websocket": AuthMiddlewareStack(
            URLRouter(
                app.routing.websocket_urlpatterns  # Load WebSocket routes from app
            )
        ),
    }
)

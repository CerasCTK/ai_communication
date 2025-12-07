"""
URL configuration for this application.

This module defines the URL patterns that map incoming HTTP requests
to the appropriate view functions within the app
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home")
]

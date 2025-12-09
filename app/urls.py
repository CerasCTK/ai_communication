"""
URL configuration for this application.

This module defines the URL patterns that map incoming HTTP requests
to the appropriate view functions within the app
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("select_topic", views.select_topic, name="select_topic"),
    path("speaking", views.speaking, name="speaking")
]

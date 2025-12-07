"""
View functions for the main application.

This module defines the HTTP endpoints used to render responses
for the root page of the application
"""

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """
    Handle requests to the home page
    """
    return render(request, "app/home.html")

"""
View functions for the main application.

This module defines the HTTP endpoints used to render responses
for the root page of the application
"""

from django.http import HttpResponse, HttpRequest


def home(_request: HttpRequest) -> HttpResponse:
    """
    Handle requests to the home page
    """
    return HttpResponse("Hello world!")

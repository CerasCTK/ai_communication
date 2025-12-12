"""
Application configuration for the 'app' Django application.

This module defines the LearningAppConfig subclass used by Django to identify
and configure the application at startup.
"""

from django.apps import AppConfig


class LearningAppConfig(AppConfig):
    """
    Configuration class for the 'app' Django application.

    Attributes:
        default_auto_field (str): Specifies the type of primary key field to use
            for automatically generated model primary keys.
        name (str): The full Python path to the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

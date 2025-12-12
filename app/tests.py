"""
Test suite for the 'app' Django application.

This module includes tests for the home view to ensure
it returns the correct HTTP response and content.
"""

from django.test import SimpleTestCase
from django.urls import reverse


class HomeViewTests(SimpleTestCase):
    """Tests for the home page view."""

    def test_home_status_code(self) -> None:
        """Home page should return HTTP 200."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self) -> None:
        """Home page should use the app/home.html template."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "app/home.html")

    def test_home_contains_basic_content(self) -> None:
        """Home page should contain expected base content."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "AI Communication")

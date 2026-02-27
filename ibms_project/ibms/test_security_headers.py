"""Tests to verify security headers are present in HTTP responses."""
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class SecurityHeadersTest(TestCase):
    """Test that security headers are properly configured."""

    def setUp(self):
        """Set up test client and create test user."""
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_x_frame_options_header(self):
        """Test that X-Frame-Options header is set to DENY."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("site_home"))
        self.assertIn("X-Frame-Options", response)
        self.assertEqual(response["X-Frame-Options"], "DENY")

    def test_content_security_policy_header(self):
        """Test that Content-Security-Policy header is present."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("site_home"))
        self.assertIn("Content-Security-Policy", response)
        # Verify it contains at least the default-src directive
        self.assertIn("default-src", response["Content-Security-Policy"])

    def test_hsts_header(self):
        """Test that Strict-Transport-Security header is present."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("site_home"))
        self.assertIn("Strict-Transport-Security", response)
        # Verify it contains max-age
        self.assertIn("max-age", response["Strict-Transport-Security"])

"""Performance baseline tests for critical views."""
import time
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class PerformanceBaselineTest(TestCase):
    """Test that critical views meet performance thresholds."""

    HOMEPAGE_THRESHOLD_MS = 500  # Homepage must respond in under 500ms

    def setUp(self):
        """Set up test client and create test user."""
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_homepage_response_time(self):
        """Test that homepage responds within 500ms threshold."""
        self.client.login(username="testuser", password="testpass123")
        
        # Warm up request (to account for JIT compilation and caching)
        self.client.get(reverse("site_home"))
        
        # Measure actual request time
        start_time = time.time()
        response = self.client.get(reverse("site_home"))
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(
            elapsed_time,
            self.HOMEPAGE_THRESHOLD_MS,
            f"Homepage response time {elapsed_time:.2f}ms exceeds threshold of {self.HOMEPAGE_THRESHOLD_MS}ms"
        )

    def test_homepage_anonymous_redirect_time(self):
        """Test that anonymous user redirect is fast (< 200ms)."""
        # Anonymous users should get a quick redirect
        start_time = time.time()
        response = self.client.get(reverse("site_home"))
        elapsed_time = (time.time() - start_time) * 1000
        
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertLess(
            elapsed_time,
            200,
            f"Anonymous redirect took {elapsed_time:.2f}ms, should be faster"
        )

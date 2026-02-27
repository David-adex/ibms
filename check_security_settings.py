#!/usr/bin/env python
"""Script to verify security header settings are configured."""
import os
import sys

# Set the database URL to use SQLite for testing
os.environ['DATABASE_URL'] = 'sqlite:////:memory:'
os.environ['DEBUG'] = 'False'

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibms_project.settings')
import django
django.setup()

from django.conf import settings

# Verify security settings
print("=== Security Settings Verification ===")
print(f"X_FRAME_OPTIONS: {getattr(settings, 'X_FRAME_OPTIONS', 'NOT SET')}")
print(f"SECURE_HSTS_SECONDS: {getattr(settings, 'SECURE_HSTS_SECONDS', 'NOT SET')}")
print(f"SECURE_HSTS_INCLUDE_SUBDOMAINS: {getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', 'NOT SET')}")
print(f"SECURE_HSTS_PRELOAD: {getattr(settings, 'SECURE_HSTS_PRELOAD', 'NOT SET')}")
print(f"SECURE_CONTENT_SECURITY_POLICY: {getattr(settings, 'SECURE_CONTENT_SECURITY_POLICY', 'NOT SET')}")
print(f"SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'NOT SET')}")

print("\n=== Middleware Configuration ===")
for mw in settings.MIDDLEWARE:
    if 'security' in mw.lower() or 'click' in mw.lower():
        print(f"  {mw}")

# Now test a simple request
print("\n=== Running Security Header Tests ===")
from django.test import Client
from django.contrib.auth import get_user_model

client = Client()
User = get_user_model()

# Create test user
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user(username='testuser', password='testpass')

# Login and make request
client.login(username='testuser', password='testpass')
response = client.get('/')

print(f"\nResponse Status: {response.status_code}")
print("\nSecurity Headers in Response:")
for header in ['X-Frame-Options', 'Content-Security-Policy', 'Strict-Transport-Security']:
    value = response.get(header, 'NOT PRESENT')
    print(f"  {header}: {value if value != 'NOT PRESENT' else '❌ ' + value}")
    if value != 'NOT PRESENT':
        print(f"    ✓ Present")

#!/usr/bin/env python
"""Test runner script with coverage measurement."""
import os
import sys
import django

# Set the database URL to use SQLite for testing
os.environ['DATABASE_URL'] = 'sqlite:////:memory:'
os.environ['DEBUG'] = 'False'

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibms_project.settings')
django.setup()

# Override storage backend to skip manifest requirement
from django.conf import settings
settings.STORAGES['staticfiles']['BACKEND'] = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Now run the tests with coverage
from django.core.management import execute_from_command_line
import coverage

# Start coverage measurement
cov = coverage.Coverage(source=['ibms_project'])
cov.start()

if __name__ == '__main__':
    try:
        execute_from_command_line([
            'manage.py',
            'test',
            'ibms.test_security_headers',
            'ibms.test_performance',
            '-v', '2'
        ])
    finally:
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        print("\n" + "="*70)
        print("CODE COVERAGE REPORT")
        print("="*70)
        cov.report()

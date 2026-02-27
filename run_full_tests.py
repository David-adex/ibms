#!/usr/bin/env python
"""Comprehensive test runner covering all tests with coverage reporting."""
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
        # Run ALL tests: views, security headers, performance, and sfm
        print("\n" + "="*80)
        print("RUNNING COMPREHENSIVE TEST SUITE")
        print("="*80 + "\n")
        exit_code = execute_from_command_line([
            'manage.py',
            'test',
            'ibms.test_views',
            'ibms.test_security_headers',
            'ibms.test_performance',
            'sfm.tests',
            '--verbosity', '2'
        ])
    finally:
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        print("\n" + "="*80)
        print("COMPLETE CODE COVERAGE REPORT")
        print("="*80)
        cov.report()
        print("\nTest run completed!")

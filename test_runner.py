#!/usr/bin/env python
"""Simple comprehensive test runner."""
import os
import sys
import django

os.environ['DATABASE_URL'] = 'sqlite:////:memory:'
os.environ['DEBUG'] = 'False'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibms_project.settings')
django.setup()

from django.conf import settings
settings.STORAGES['staticfiles']['BACKEND'] = 'django.contrib.staticfiles.storage.StaticFilesStorage'

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("\n" + "="*80)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("="*80 + "\n")
    
    try:
        execute_from_command_line([
            'manage.py',
            'test',
            'ibms.test_views',
            'ibms.test_security_headers',
            'ibms.test_performance',
            'sfm.tests',
            '--verbosity', '1'
        ])
        print("\n✅ ALL TESTS PASSED!\n")
    except SystemExit as e:
        if e.code != 0:
            print(f"\n❌ TESTS FAILED with exit code {e.code}\n")
        else:
            print("\n✅ TEST RUN COMPLETED SUCCESSFULLY!\n")

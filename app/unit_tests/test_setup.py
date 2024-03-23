import os
import django


def setup():
    if os.environ.get('UNIT_TESTS_SETUP_COMPLETED', 'False') == 'True':
        return

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unit_tests.settings')
    os.environ.setdefault('UNIT_TESTS_SETUP_COMPLETED', 'True')
    django.setup()

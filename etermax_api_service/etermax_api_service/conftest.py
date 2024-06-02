import os
import django


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etermax_api_service.settings.test')
    django.setup()

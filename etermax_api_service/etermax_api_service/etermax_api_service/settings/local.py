"""
Django settings for etermax_api_service project.

Generated by 'django-admin startproject' using Django 3.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from .base import *


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.dummy'
   }
}

REDIS_LOCATION = f"redis://{os.environ.get('REDIS_HOST', '')}:{os.environ.get('REDIS_PORT', '')}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Additional Sessions Config
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Redis configuration for Celery
CELERY_BROKER_URL = REDIS_LOCATION

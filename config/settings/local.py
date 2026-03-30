from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# SQLITE (LOCAL DATABASE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Faster static handling for development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

print("USING LOCAL SETTINGS ✅")
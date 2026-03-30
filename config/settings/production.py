# POSTGRES DATABASE (Render ENV VARIABLES)
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ['.onrender.com']


# POSTGRES DATABASE (Render ENV VARIABLES)
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}


# SECURITY SETTINGS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Recommended for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import cloudinary

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'




# SECURITY SETTINGS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Recommended for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

import cloudinary

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


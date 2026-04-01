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

import cloudinary

cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME', 'dvuv7kz5p'),
    api_key=os.environ.get('CLOUDINARY_API_KEY', '849246665983819'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET', 'f97l2q384M_FCzHSpN2OnK7aVzY')
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

print("USING LOCAL SETTINGS ✅")
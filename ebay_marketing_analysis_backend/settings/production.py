from settings.base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('PRODUCTION_DATABASE_NAME'),
        'USER': os.getenv('PRODUCTION_DATABASE_USER'),
        'PASSWORD': os.getenv('PRODUCTION_DATABASE_PASSWORD'),
        'HOST': os.getenv('PRODUCTION_DATABASE_HOST'),
        'PORT': os.getenv('PRODUCTION_DATABASE_PORT'),
    }
}
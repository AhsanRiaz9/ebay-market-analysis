from settings.base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('LOCAL_DATABASE_NAME'),
        'USER': os.getenv('LOCAL_DATABASE_USER'),
        'PASSWORD': os.getenv('LOCAL_DATABASE_PASSWORD'),
        'HOST': os.getenv('LOCAL_DATABASE_HOST'),
        'PORT': os.getenv('LOCAL_DATABASE_PORT'),
    }
}
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'productdb',
        'USER': 'postgres',
        'PASSWORD': '0000',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

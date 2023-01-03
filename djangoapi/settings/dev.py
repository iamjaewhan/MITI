from .base import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = get_secret("DATABASE")
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

## LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

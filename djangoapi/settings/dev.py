from .base import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = get_secret("DATABASE")
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

from .base import *


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = get_secret("DATABASE")

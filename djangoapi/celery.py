import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoapi.settings.dev')

app = Celery('miti',
             broker='amqp://miti:miti@localhost/',
             include=['games.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
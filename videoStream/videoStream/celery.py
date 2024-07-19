import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoStream.settings')

app = Celery('videoStream')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def debug_task():
    return

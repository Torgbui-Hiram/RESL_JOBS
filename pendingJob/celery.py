from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from .settings import CELERY_BEAT_SCHEDULE


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pendingJob.settings')

app = Celery('pendingJob')
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

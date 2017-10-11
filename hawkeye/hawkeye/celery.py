from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hawkeye.settings.dev')

from django.conf import settings

app = Celery('quicksilverApi',backend='redis://localhost:6379/0')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.timezone = 'UTC'

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    'count':{
        'task': 'api.tasks.run_delay_task',
        'schedule': 1.0,
        'args': ()
    }
}


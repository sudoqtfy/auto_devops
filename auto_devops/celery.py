from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_devops.settings')

from django.conf import settings

app = Celery('auto_devops')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
#    BROKER_URL = 'redis://127.0.0.1/0',
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_RESULT_SERIALIZER="json",
    CELERY_TASK_SERIALIZER="json",
    CELERY_CHORD_PROPAGATES=False,
)

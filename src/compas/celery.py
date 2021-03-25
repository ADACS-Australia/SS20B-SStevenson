from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compas.settings')

# Celery app and include tasks from e.g. compasweb.utils if necessary
app = Celery('compas')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# Retrieve task timout limits from environment file
# app.conf.update(
#     task_soft_time_limit = 300,
#     task_time_limit = 330,
# )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

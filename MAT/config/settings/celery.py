from __future__ import absolute_import
import os
from celery import Celery
from MAT.config.settings import local

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MAT.config.settings.base')
app = Celery('MAT.config.settings')
app.config_from_object('MAT.config.settings.base')
app.autodiscover_tasks(lambda: local.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

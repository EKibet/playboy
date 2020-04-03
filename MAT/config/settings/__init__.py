from __future__ import absolute_import

# this will m ake sure the app is always imported when django starts that shared task will use this app

from .celery import app as celery_app
__all__ = ('celery_app',)

from .base import *


DEBUG = env.bool('DJANGO_DEBUG', default=True)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECRET_KEY = env('SECRET_KEY',
                 default='lx9joase75e!kb+8*2=z6vs!a+@)c2q*hbhwpb9&0kv31et%ac')
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = ['*']

BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
# INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)

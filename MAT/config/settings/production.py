from .base import *

SECRET_KEY = env('SECRET_KEY')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
DJANGO_DEBUG = False
DJANGO_READ_DOT_ENV_FILE = False

from .base import *

ALLOWED_HOSTS = []
SECRET_KEY = env('SECRET_KEY')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

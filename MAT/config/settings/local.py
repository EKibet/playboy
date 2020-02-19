from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=True)

SECRET_KEY = env('SECRET_KEY',
                 default='lx9joase75e!kb+8*2=z6vs!a+@)c2q*hbhwpb9&0kv31et%ac')
ALLOWED_HOSTS = ['127.0.0.1', '206.189.212.117']

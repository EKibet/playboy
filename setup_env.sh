#!/bin/sh

echo DEBUG=0 >> .env
echo SQL_ENGINE=django.db.backends.postgresql >> .env
echo DATABASE=postgres >> .env


echo DJANGODIR=$DJANGODIR >> .env
echo SECRET_KEY=$SECRET_KEY >> .env
echo SENTRY_DSN=$SENTRY_DSN >> .env
echo DATABASE_URL=$DATABASE_URL >> .env
echo DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE >> .env
echo DJANGO_WSGI_MODULE=$DJANGO_WSGI_MODULE >> .env
echo DJANGO_READ_DOT_ENV_FILE=$DJANGO_READ_DOT_ENV_FILE >> .env
echo PUNCTUAL_TIME=$PUNCTUAL_TIME >> .env
echo CHECKOUT_TIME=$CHECKOUT_TIME >> .env
echo STUDENTS_PASSWORD=$STUDENTS_PASSWORD >> .env
echo EMAIL_HOST=$EMAIL_HOST >> .env
echo EMAIL_PASSWORD=$EMAIL_PASSWORD >> .env
echo EMAIL_HOST_USER=$EMAIL_HOST_USER >> .env
echo EMAIL_PORT=$EMAIL_PORT >> .env
echo APP_BASE_URL=$APP_BASE_URL >> .env
echo CLOUD_NAME=$CLOUD_NAME >> .env
echo API_KEY=$API_KEY >> .env
echo API_SECRET=$API_SECRET >> .env
echo CLOUD_FOLDER=$CLOUD_FOLDER >> .env
echo GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID >> .env
echo web_image=$image:web  >> .env
echo nginx_image=$image:nginx  >> .env
echo CI_REGISTRY_USER=$CI_REGISTRY_USER   >> .env
echo CI_JOB_TOKEN=$CI_JOB_TOKEN  >> .env
echo CI_REGISTRY=$CI_REGISTRY  >> .env
echo SQL_DATABASE=$SQL_DATABASE >> .env
echo SQL_USER=$SQL_USER >> .env
echo SQL_PASSWORD=$SQL_PASSWORD >> .env
echo image=$CI_REGISTRY/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME >> .env
echo SQL_HOST=$SQL_HOST >> .env
echo SQL_PORT=$SQL_PORT >> .env





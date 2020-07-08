# pull official base image
FROM python:3.7.8-alpine

# set work directory
WORKDIR /srv/mat-api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps \
    && apk install python3-pip

# install dependencies
RUN pip3 install pipenv
RUN pipenv --python 3.7
RUN exit
RUN pipenv shell
COPY ./Pipfile.lock /srv/mat-api/Pipfile.lock
RUN pipenv sync

# copy entrypoint-prod.sh
COPY ./entrypoint.sh /srv/mat-api/entrypoint.sh

# copy project
COPY . /srv/mat-api

# run entrypoint.prod.sh
ENTRYPOINT ["/srv/mat-api/MAT/entrypoint.sh"]
#!/usr/bin/env bash

echo $DJANGO_SETTINGS_MODULE

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=4
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

if [ -z "${GUNICORN_TIMEOUT}" ]; then
    GUNICORN_TIMEOUT=120
fi

if [ -z "${DJANGO_DB_PORT}" ]; then
    DJANGO_DB_PORT=3306
fi

set -x

wait-port ${DJANGO_DB_HOST}:${DJANGO_DB_PORT} -t 15000

python manage.py migrate

gunicorn \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    --timeout=${GUNICORN_TIMEOUT} \
    student_explorer.wsgi:application

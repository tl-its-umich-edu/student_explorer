#!/usr/bin/env bash

echo $DJANGO_SETTINGS_MODULE

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=4
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

set -x

python manage.py migrate

gunicorn \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    --timeout=60 \
    student_explorer.wsgi:application

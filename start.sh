#!/usr/bin/env bash

if [ -z "${SETTINGS_MODULE}" ]; then
    SETTINGS_MODULE=student_explorer.settings.env
fi

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=2
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

set -x

python manage.py migrate --settings "${SETTINGS_MODULE}"
python manage.py collectstatic --settings "${SETTINGS_MODULE}" \
    --noinput

gunicorn --settings "${SETTINGS_MODULE}" \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    student_explorer.wsgi:application

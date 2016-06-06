#!/usr/bin/env bash

if [ ! -e student_explorer/local/settings.py ] && [ -z "${DJANGO_SETTINGS_MODULE}" ]; then
    # If the local settings module doesn't exists and the environment doesn't
    # define a settings module, we will use the base settings.
    export DJANGO_SETTINGS_MODULE=student_explorer.settings
fi

echo $DJANGO_SETTINGS_MODULE

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=4
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

set -x

gunicorn \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    student_explorer.wsgi:application

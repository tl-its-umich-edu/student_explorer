#!/usr/bin/env bash

if [ -z "${DJANGO_SETTINGS_MODULE}" ]; then
    export DJANGO_SETTINGS_MODULE=student_explorer.settings.base
fi

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

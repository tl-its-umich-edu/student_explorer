#!/usr/bin/env bash

if [ -z "${DJANGO_SETTINGS_MODULE}" ]; then
    export DJANGO_SETTINGS_MODULE=student_explorer.settings
fi

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=4
fi

if [ -z "${GUNICORN_PORT}" ]; then
    GUNICORN_PORT=8000
fi

if [ -z "${GUNICORN_SCRIPT_NAME}" ]; then
    GUNICORN_SCRIPT_NAME=
fi

set -x

export SCRIPT_NAME=${GUNICORN_SCRIPT_NAME}

gunicorn \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    student_explorer.wsgi:application

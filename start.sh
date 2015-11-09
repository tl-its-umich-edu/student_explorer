#!/usr/bin/env bash

if [ -z "${GUNICORN_WORKERS}" ]; then
    GUNICORN_WORKERS=2
fi

python manage.py migrate
# python manage.py collectstatic

gunicorn --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:80 student_explorer.wsgi:application

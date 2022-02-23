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

if [ "${GUNICORN_RELOAD}" ]; then
    GUNICORN_RELOAD="--reload"
else
    GUNICORN_RELOAD=""
fi

set -x

python manage.py migrate

if [ "${CACHE_BACKEND:-""}" == "django.core.cache.backends.db.DatabaseCache" ]; then
    echo "Database cache set; creating cache table"
    python manage.py createcachetable
fi

if [ "${PTVSD_ENABLE:-"False"}" == "False" ]; then
    # Start Gunicorn processes
    echo Starting Gunicorn for production

    # application pod
    exec gunicorn student_explorer.wsgi:application \
        --bind 0.0.0.0:${GUNICORN_PORT} \
        --workers="${GUNICORN_WORKERS}" \
        --timeout="${GUNICORN_TIMEOUT}" \
        ${GUNICORN_RELOAD}
else
    # Currently ptvsd doesn't work with gunicorn
    # https://github.com/Microsoft/vscode-python/issues/2138
    echo Starting Runserver for development
    export PYTHONPATH="/usr/src/app:$PYTHONPATH"
    export DJANGO_SETTINGS_MODULE=student_explorer.settings
    exec django-admin runserver --ptvsd 0.0.0.0:${GUNICORN_PORT}
fi
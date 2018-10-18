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

set -x

dockerize -wait tcp://${DJANGO_DB_HOST}:${DJANGO_DB_PORT} -timeout 15s

python manage.py migrate

if [ -z "{$LOCALHOST_DEV}" ]
then
    echo "Running on Production"
else
    echo "Running on Dev, setting up some test data"
    python manage.py loaddata student_explorer/fixtures/dev_users.json
    mysql -h ${DJANGO_DB_HOST} -u ${DJANGO_DB_USER} -p${DJANGO_DB_PASSWORD} ${DJANGO_DB_NAME} < seumich/fixtures/dev_data_drop_create_and_insert.sql
    
fi

gunicorn \
    --workers="${GUNICORN_WORKERS}" \
    --bind=0.0.0.0:${GUNICORN_PORT} \
    --timeout=${GUNICORN_TIMEOUT} \
    student_explorer.wsgi:application

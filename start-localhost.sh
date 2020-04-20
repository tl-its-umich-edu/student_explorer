#!/usr/bin/env bash

# These are only needed for dev
echo "Running on Dev, setting up some test data"
while ! nc -z ${DJANGO_DB_HOST} ${DJANGO_DB_PORT}; do   
  sleep 1 # wait 1 second before check again
done

python manage.py migrate

python manage.py loaddata student_explorer/fixtures/dev_users.json
mysql -h ${DJANGO_DB_HOST} -u ${DJANGO_DB_USER} -p${DJANGO_DB_PASSWORD} ${DJANGO_DB_NAME} < seumich/fixtures/dev_data_drop_create_and_insert.sql
python manage.py import_manage_fixtures

. start.sh

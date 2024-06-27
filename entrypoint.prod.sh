#!/bin/sh

if [ "$DATABASE" = "his_db_local" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"
python manage.py migrate --fake user_authentication zero
python manage.py makemigrations user_authentication
python manage.py migrate

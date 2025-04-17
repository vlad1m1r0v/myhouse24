#!/bin/sh

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Creating groups..."
python manage.py creategroups

exec "$@"
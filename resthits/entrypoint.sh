#!/bin/sh

echo "Waiting for PostgreSQL to start..."

sleep 10

echo "PostgreSQL is up - making migrations..."

python manage.py makemigrations
python manage.py migrate

echo "Migrations applied - starting server..."
exec "$@"

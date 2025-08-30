#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating initial users..."
python manage.py create_initial_users || echo "Users already exist or error creating users"

echo "Setting up rooms..."
python manage.py setup_rooms || echo "Rooms already exist or error setting up rooms"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting gunicorn server..."
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 hotel_pms.wsgi:application
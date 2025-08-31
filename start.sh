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

echo "Starting background services..."

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A hotel_pms worker --loglevel=info --detach

# Start Celery beat scheduler in background  
echo "Starting Celery beat scheduler..."
celery -A hotel_pms beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach

# Give services time to start
sleep 5

echo "Starting gunicorn server..."
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 hotel_pms.wsgi:application
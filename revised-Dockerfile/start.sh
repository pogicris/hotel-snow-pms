#!/bin/bash
set -e

echo "🚀 Starting Hotel Snow PMS Setup..."

echo "📋 Running database migrations..."
python manage.py migrate

echo "🏨 Setting up rooms and room types..."
python setup_database.py

echo "🎯 Starting Gunicorn Server..."
exec gunicorn --bind 0.0.0.0:10000 hotel_pms.wsgi:application
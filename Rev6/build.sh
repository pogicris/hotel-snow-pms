#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install build tools
pip install --upgrade pip setuptools wheel

# Install PostgreSQL development headers (if available)
apt-get update || true
apt-get install -y libpq-dev gcc python3-dev || true

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Setup initial data
python manage.py setup_rooms
python manage.py create_initial_users
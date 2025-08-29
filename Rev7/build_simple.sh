#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Setup initial data
echo "Setting up rooms and users..."
python manage.py setup_rooms || echo "Rooms already exist"
python manage.py create_initial_users || echo "Users already exist"

echo "Build completed successfully!"
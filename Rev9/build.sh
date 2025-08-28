#!/usr/bin/env bash
# Render.com build script for Hotel PMS Rev9
set -o errexit

echo "🚀 Building Hotel PMS Rev9 for Render..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input

# Initialize production data
python init_production.py

echo "✅ Rev9 build complete!"
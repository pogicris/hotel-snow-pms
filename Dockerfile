# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
python manage.py migrate --noinput\n\
echo "Creating initial users..."\n\
python manage.py create_initial_users || echo "Users already exist or error creating users"\n\
echo "Setting up rooms..."\n\
python manage.py setup_rooms || echo "Rooms already exist or error setting up rooms"\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput --clear\n\
echo "Starting gunicorn server..."\n\
gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 hotel_pms.wsgi:application\n' > /app/start.sh && chmod +x /app/start.sh

# Run the application with migrations
CMD ["/app/start.sh"]
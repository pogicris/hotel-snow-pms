FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=hotel_pms.settings

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create .env file from environment variables
RUN echo "DEBUG=${DEBUG:-False}" > .env && \
    echo "SECRET_KEY=${SECRET_KEY}" >> .env && \
    echo "ALLOWED_HOSTS=${ALLOWED_HOSTS:-*}" >> .env && \
    echo "DATABASE_URL=${DATABASE_URL:-sqlite:///db.sqlite3}" >> .env

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "hotel_pms.wsgi:application"]
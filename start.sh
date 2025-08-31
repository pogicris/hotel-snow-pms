#!/bin/bash
set -e

echo "🚀 Hotel Snow PMS - Starting Deployment..."
echo "================================================"

# Step 1: Database Setup
echo "📊 Step 1: Database Setup"
echo "Running database migrations..."
python manage.py migrate --noinput
if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully"
else
    echo "❌ Database migrations failed"
    exit 1
fi

echo ""
echo "👥 Step 2: Initial Data Setup"
echo "Creating initial users..."
if python manage.py create_initial_users; then
    echo "✅ Initial users created/verified"
else
    echo "⚠️ Users setup completed with warnings (may already exist)"
fi

echo "Setting up rooms..."
if python manage.py setup_rooms; then
    echo "✅ Rooms setup completed"
else
    echo "⚠️ Rooms setup completed with warnings (may already exist)"
fi

echo ""
echo "📁 Step 3: Static Files Collection"
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
if [ $? -eq 0 ]; then
    echo "✅ Static files collected successfully"
else
    echo "❌ Static files collection failed"
    exit 1
fi

echo ""
echo "⚙️ Step 4: Background Services Setup"

# Check if Redis is available for Celery
if [ -z "$REDIS_URL" ]; then
    echo "⚠️ Warning: REDIS_URL not set - Celery services will not start"
    echo "⚠️ Automatic backups will be disabled until Redis is configured"
    CELERY_ENABLED=false
else
    echo "✅ Redis URL detected - Celery services will start"
    CELERY_ENABLED=true
fi

if [ "$CELERY_ENABLED" = true ]; then
    # Start Celery worker in background
    echo "Starting Celery worker..."
    celery -A hotel_pms worker --loglevel=info --detach --pidfile=/tmp/celery_worker.pid
    if [ $? -eq 0 ]; then
        echo "✅ Celery worker started successfully"
    else
        echo "❌ Celery worker failed to start"
        exit 1
    fi
    
    # Start Celery beat scheduler in background  
    echo "Starting Celery beat scheduler..."
    celery -A hotel_pms beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach --pidfile=/tmp/celery_beat.pid
    if [ $? -eq 0 ]; then
        echo "✅ Celery beat scheduler started successfully"
    else
        echo "❌ Celery beat scheduler failed to start"
        exit 1
    fi
    
    # Give services time to start and verify they're running
    echo "Waiting for services to initialize..."
    sleep 8
    
    # Check if services are still running
    if [ -f /tmp/celery_worker.pid ] && kill -0 `cat /tmp/celery_worker.pid` 2>/dev/null; then
        echo "✅ Celery worker is running (PID: $(cat /tmp/celery_worker.pid))"
    else
        echo "⚠️ Celery worker may not be running properly"
    fi
    
    if [ -f /tmp/celery_beat.pid ] && kill -0 `cat /tmp/celery_beat.pid` 2>/dev/null; then
        echo "✅ Celery beat scheduler is running (PID: $(cat /tmp/celery_beat.pid))"
    else
        echo "⚠️ Celery beat scheduler may not be running properly"
    fi
fi

echo ""
echo "🌐 Step 5: Web Server Startup"
echo "Starting Gunicorn web server..."
echo "Server will be available at: https://hotel-snow-pms-docker.onrender.com"
echo "================================================"

exec gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --access-logfile - --error-logfile - hotel_pms.wsgi:application
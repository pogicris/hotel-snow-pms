#!/bin/bash

echo "🔍 Hotel Snow PMS - Service Status Monitor"
echo "=========================================="

# Check web server
echo "🌐 Web Server Status:"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health/ | grep -q "200"; then
    echo "✅ Web server is responding (Port 8000)"
else
    echo "❌ Web server is not responding"
fi

echo ""
echo "⚙️ Background Services:"

# Check Celery Worker
if [ -f /tmp/celery_worker.pid ] && kill -0 `cat /tmp/celery_worker.pid` 2>/dev/null; then
    echo "✅ Celery Worker is running (PID: $(cat /tmp/celery_worker.pid))"
else
    echo "❌ Celery Worker is not running"
fi

# Check Celery Beat
if [ -f /tmp/celery_beat.pid ] && kill -0 `cat /tmp/celery_beat.pid` 2>/dev/null; then
    echo "✅ Celery Beat Scheduler is running (PID: $(cat /tmp/celery_beat.pid))"
else
    echo "❌ Celery Beat Scheduler is not running"
fi

echo ""
echo "📊 Database Connection:"
if python manage.py check --database default >/dev/null 2>&1; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed"
fi

echo ""
echo "🔧 Environment Check:"
if [ -n "$REDIS_URL" ]; then
    echo "✅ Redis URL configured: ${REDIS_URL:0:20}..."
else
    echo "⚠️ Redis URL not configured"
fi

if [ -n "$DEBUG" ]; then
    echo "🐛 Debug mode: $DEBUG"
else
    echo "🔒 Debug mode: False (default)"
fi

echo ""
echo "📋 Recent Backup Activity:"
python manage.py shell -c "
from rooms.models import DataBackup
from django.utils import timezone
recent = DataBackup.objects.filter(
    created_at__gte=timezone.now() - timezone.timedelta(hours=1)
).count()
total = DataBackup.objects.count()
print(f'Recent backups (last hour): {recent}')
print(f'Total backups in system: {total}')
"

echo "=========================================="
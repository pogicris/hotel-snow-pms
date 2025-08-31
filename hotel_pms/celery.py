import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')

app = Celery('hotel_pms')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'automatic-backup-every-10-minutes': {
        'task': 'rooms.tasks.create_automatic_backup',
        'schedule': 600.0,  # 600 seconds = 10 minutes
    },
    'cleanup-old-backups-hourly': {
        'task': 'rooms.tasks.cleanup_old_backup_files',
        'schedule': 3600.0,  # 3600 seconds = 1 hour
    },
    'backup-health-check-daily': {
        'task': 'rooms.tasks.backup_system_health_check',
        'schedule': 86400.0,  # 86400 seconds = 24 hours
    },
}

app.conf.timezone = 'Asia/Manila'
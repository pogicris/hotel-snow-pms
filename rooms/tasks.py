try:
    from celery import shared_task
except ImportError:
    # Celery not available, create a dummy decorator
    def shared_task(func):
        return func
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import logging
from .backup_utils import create_backup_record, cleanup_old_backups
from .models import ActivityLog

logger = logging.getLogger(__name__)


@shared_task
def create_automatic_backup():
    """
    Create automatic backup every 10 minutes
    This task is scheduled to run every 10 minutes
    """
    try:
        # Create the backup
        backup = create_backup_record(
            backup_type='AUTO',
            notes=f'Automatic backup created at {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
        
        # Log the activity
        ActivityLog.objects.create(
            action=f'Automatic backup created: {backup.file_name}',
            timestamp=timezone.now(),
            path='/backup/auto',
            method='TASK'
        )
        
        logger.info(f"Automatic backup created successfully: {backup.file_name}")
        
        return {
            'success': True,
            'backup_id': backup.id,
            'file_name': backup.file_name,
            'booking_count': backup.booking_count
        }
        
    except Exception as e:
        logger.error(f"Error creating automatic backup: {str(e)}")
        
        # Log the error
        ActivityLog.objects.create(
            action=f'Automatic backup failed: {str(e)}',
            timestamp=timezone.now(),
            path='/backup/auto',
            method='TASK'
        )
        
        return {
            'success': False,
            'error': str(e)
        }


@shared_task
def cleanup_old_backup_files():
    """
    Clean up old backup files every hour
    Remove automatic backups older than 24 hours (keeping 144 backups max)
    """
    try:
        deleted_count = cleanup_old_backups()
        
        # Log the cleanup activity
        ActivityLog.objects.create(
            action=f'Backup cleanup completed: {deleted_count} old backups removed',
            timestamp=timezone.now(),
            path='/backup/cleanup',
            method='TASK'
        )
        
        logger.info(f"Backup cleanup completed: {deleted_count} old backups removed")
        
        return {
            'success': True,
            'deleted_count': deleted_count
        }
        
    except Exception as e:
        logger.error(f"Error during backup cleanup: {str(e)}")
        
        # Log the error
        ActivityLog.objects.create(
            action=f'Backup cleanup failed: {str(e)}',
            timestamp=timezone.now(),
            path='/backup/cleanup',
            method='TASK'
        )
        
        return {
            'success': False,
            'error': str(e)
        }


@shared_task
def backup_system_health_check():
    """
    Daily health check for backup system
    Verify that backups are being created regularly
    """
    try:
        from .models import DataBackup
        
        # Check if we have recent backups (within last hour)
        recent_backups = DataBackup.objects.filter(
            backup_type='AUTO',
            created_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).count()
        
        if recent_backups == 0:
            # No recent backups - this might indicate a problem
            ActivityLog.objects.create(
                action='Backup system alert: No automatic backups in the last hour',
                timestamp=timezone.now(),
                path='/backup/health',
                method='TASK'
            )
            
            logger.warning("Backup system health check: No automatic backups in the last hour")
            
            return {
                'success': False,
                'message': 'No recent automatic backups found',
                'recent_backups': recent_backups
            }
        
        # System is healthy
        total_backups = DataBackup.objects.count()
        auto_backups = DataBackup.objects.filter(backup_type='AUTO').count()
        
        ActivityLog.objects.create(
            action=f'Backup system health check passed: {recent_backups} recent, {total_backups} total backups',
            timestamp=timezone.now(),
            path='/backup/health',
            method='TASK'
        )
        
        return {
            'success': True,
            'recent_backups': recent_backups,
            'total_backups': total_backups,
            'auto_backups': auto_backups
        }
        
    except Exception as e:
        logger.error(f"Error during backup health check: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
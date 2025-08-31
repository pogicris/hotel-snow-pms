import threading
import time
from django.utils import timezone
from django.conf import settings
from django.core.management import call_command
from rooms.models import DataBackup, ActivityLog
import logging

logger = logging.getLogger(__name__)

class BackupScheduler:
    """
    Simple backup scheduler that runs in background thread
    Fallback when Celery/Redis is not available
    """
    
    def __init__(self):
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the backup scheduler"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Backup scheduler started")
        
    def stop(self):
        """Stop the backup scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Backup scheduler stopped")
        
    def _run_scheduler(self):
        """Main scheduler loop"""
        logger.info("Starting backup scheduler loop...")
        
        while self.running:
            try:
                # Check if it's time for a backup (every 10 minutes)
                if self._should_create_backup():
                    logger.info("Creating automatic backup...")
                    self._create_backup()
                    
                # Sleep for 60 seconds before checking again
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in backup scheduler: {str(e)}")
                # Continue running even if there's an error
                time.sleep(60)
                
    def _should_create_backup(self):
        """Check if we should create a backup now"""
        try:
            # Get the last automatic backup
            last_backup = DataBackup.objects.filter(
                backup_type='AUTO'
            ).order_by('-created_at').first()
            
            if not last_backup:
                # No backups exist, create one
                return True
                
            # Check if last backup was more than 10 minutes ago
            time_since_last = timezone.now() - last_backup.created_at
            return time_since_last.total_seconds() >= (10 * 60)  # 10 minutes
            
        except Exception as e:
            logger.error(f"Error checking backup schedule: {str(e)}")
            return False
            
    def _create_backup(self):
        """Create an automatic backup"""
        try:
            # Use the management command to create backup
            call_command('run_auto_backup')
            logger.info("Automatic backup created successfully")
            
        except Exception as e:
            logger.error(f"Error creating automatic backup: {str(e)}")

# Global scheduler instance
_scheduler = None

def start_backup_scheduler():
    """Start the backup scheduler if not already running"""
    global _scheduler
    
    # Only start if we're not in a test environment and Redis is not available
    if settings.DEBUG or _scheduler is not None:
        return
        
    # Check if Celery is available and working
    redis_url = getattr(settings, 'CELERY_BROKER_URL', None)
    if redis_url and 'redis' in redis_url:
        # Celery should handle backups
        logger.info("Redis/Celery detected, skipping thread-based scheduler")
        return
    
    _scheduler = BackupScheduler()
    _scheduler.start()
    logger.info("Thread-based backup scheduler started as fallback")

def stop_backup_scheduler():
    """Stop the backup scheduler"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
        _scheduler = None
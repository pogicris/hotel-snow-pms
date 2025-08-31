from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.core.management import call_command
from rooms.models import DataBackup
import logging
import threading

logger = logging.getLogger(__name__)

class AutoBackupMiddleware(MiddlewareMixin):
    """
    Middleware that triggers automatic backups every 10 minutes
    This is a fallback when Celery/Redis is not available
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self._last_check = None
        self._backup_lock = threading.Lock()
        super().__init__(get_response)

    def process_request(self, request):
        """Check if we need to create a backup on each request"""
        # Only check occasionally to avoid database overhead
        now = timezone.now()
        
        if self._last_check is None or (now - self._last_check).total_seconds() > 300:  # Check every 5 minutes
            self._last_check = now
            self._check_and_create_backup()
        
        return None

    def _check_and_create_backup(self):
        """Check if backup is needed and create it in background"""
        try:
            # Use lock to prevent multiple simultaneous backup attempts
            if not self._backup_lock.acquire(blocking=False):
                return
                
            try:
                # Check if we need a backup
                if self._should_create_backup():
                    # Create backup in background thread
                    thread = threading.Thread(target=self._create_backup_async, daemon=True)
                    thread.start()
                    
            finally:
                self._backup_lock.release()
                
        except Exception as e:
            logger.error(f"Error in backup middleware: {str(e)}")

    def _should_create_backup(self):
        """Check if we should create a backup now"""
        try:
            # Get the last automatic backup
            last_backup = DataBackup.objects.filter(
                backup_type='AUTO'
            ).order_by('-created_at').first()
            
            if not last_backup:
                return True
                
            # Check if last backup was more than 10 minutes ago
            time_since_last = timezone.now() - last_backup.created_at
            return time_since_last.total_seconds() >= (10 * 60)  # 10 minutes
            
        except Exception as e:
            logger.error(f"Error checking backup schedule in middleware: {str(e)}")
            return False

    def _create_backup_async(self):
        """Create backup in background thread"""
        try:
            logger.info("Creating automatic backup via middleware...")
            call_command('run_auto_backup')
            
        except Exception as e:
            logger.error(f"Error creating backup in middleware: {str(e)}")

class RequestBasedBackupTrigger(MiddlewareMixin):
    """
    Alternative backup trigger that runs on specific requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_request(self, request):
        """Trigger backup check on backup-related requests"""
        # Only trigger on backup management or dashboard requests
        if any(path in request.path for path in ['/backup-management/', '/timeline/', '/']):
            self._check_backup_async()
        
        return None

    def _check_backup_async(self):
        """Check and create backup if needed (async)"""
        try:
            # Get the last automatic backup
            last_backup = DataBackup.objects.filter(
                backup_type='AUTO'
            ).order_by('-created_at').first()
            
            if not last_backup:
                # No backups exist, create one
                threading.Thread(target=self._create_backup, daemon=True).start()
                return
                
            # Check if last backup was more than 10 minutes ago
            time_since_last = timezone.now() - last_backup.created_at
            if time_since_last.total_seconds() >= (10 * 60):  # 10 minutes
                threading.Thread(target=self._create_backup, daemon=True).start()
                
        except Exception as e:
            logger.error(f"Error in request-based backup trigger: {str(e)}")

    def _create_backup(self):
        """Create backup in background"""
        try:
            call_command('run_auto_backup')
            logger.info("Automatic backup created via request trigger")
            
        except Exception as e:
            logger.error(f"Error creating backup via request trigger: {str(e)}")
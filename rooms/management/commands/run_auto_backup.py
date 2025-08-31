from django.core.management.base import BaseCommand
from django.utils import timezone
from rooms.backup_utils import create_backup_record, cleanup_old_backups
from rooms.models import ActivityLog, DataBackup
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create automatic backup and cleanup old ones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force backup creation even if recent backup exists',
        )

    def handle(self, *args, **options):
        try:
            # Check if we should create a backup (every 10 minutes)
            if not options['force']:
                # Check for recent backups (within last 8 minutes to allow some overlap)
                recent_backup = DataBackup.objects.filter(
                    backup_type='AUTO',
                    created_at__gte=timezone.now() - timezone.timedelta(minutes=8)
                ).exists()
                
                if recent_backup:
                    self.stdout.write(
                        self.style.WARNING('Recent automatic backup exists, skipping...')
                    )
                    return

            # Create the backup
            backup = create_backup_record(
                backup_type='AUTO',
                notes=f'Automatic backup via command at {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}'
            )
            
            # Log the activity
            ActivityLog.objects.create(
                action=f'Automatic backup created via command: {backup.file_name}',
                timestamp=timezone.now(),
                path='/backup/auto-command',
                method='COMMAND'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Automatic backup created: {backup.file_name}')
            )
            self.stdout.write(f'   📊 Bookings: {backup.booking_count}')
            self.stdout.write(f'   💾 Size: {backup.get_file_size():.1f} KB')
            
            # Cleanup old backups
            deleted_count = cleanup_old_backups()
            if deleted_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'🧹 Cleaned up {deleted_count} old backups')
                )
                
                # Log cleanup activity
                ActivityLog.objects.create(
                    action=f'Backup cleanup via command: {deleted_count} old backups removed',
                    timestamp=timezone.now(),
                    path='/backup/cleanup-command',
                    method='COMMAND'
                )
            
            # Show current backup statistics
            total_backups = DataBackup.objects.count()
            auto_backups = DataBackup.objects.filter(backup_type='AUTO').count()
            
            self.stdout.write(f'📈 Current backup stats:')
            self.stdout.write(f'   Total backups: {total_backups}')
            self.stdout.write(f'   Auto backups: {auto_backups}')
            
        except Exception as e:
            logger.error(f"Error in automatic backup command: {str(e)}")
            
            # Log the error
            ActivityLog.objects.create(
                action=f'Automatic backup command failed: {str(e)}',
                timestamp=timezone.now(),
                path='/backup/auto-command',
                method='COMMAND'
            )
            
            self.stdout.write(
                self.style.ERROR(f'❌ Automatic backup failed: {str(e)}')
            )
            raise
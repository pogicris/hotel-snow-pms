from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('manage-rates/', views.manage_rates, name='manage_rates'),
    path('system-memo/', views.system_memo, name='system_memo'),
    path('activity-log/', views.activity_log_view, name='activity_log'),
    
    # Backup management URLs
    path('backup-management/', views.backup_management, name='backup_management'),
    path('export-data/', views.export_data, name='export_data'),
    path('import-data/', views.import_data, name='import_data'),
    path('manual-backup/', views.manual_backup, name='manual_backup'),
    path('trigger-auto-backup/', views.trigger_auto_backup, name='trigger_auto_backup'),
    path('download-backup/<int:backup_id>/', views.download_backup, name='download_backup'),
    path('delete-backup/<int:backup_id>/', views.delete_backup, name='delete_backup'),
]
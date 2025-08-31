from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, date
import json
from decimal import Decimal

from .models import Room, RoomType, Booking, CustomUser, SystemMemo, ActivityLog, DataBackup
from .backup_utils import export_bookings_to_excel, import_bookings_from_excel, create_backup_record

def is_admin_or_super(user):
    return user.is_authenticated and (user.user_type in ['ADMIN', 'SUPER'])

def is_super_user(user):
    return user.is_authenticated and user.user_type == 'SUPER'

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'rooms/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    today = timezone.now().date()
    
    # Get active popup memos
    popup_memos = SystemMemo.objects.filter(is_popup=True, is_active=True)
    
    # Get bookings for timeline (current 2 weeks)
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=13)
    
    bookings = Booking.objects.filter(
        Q(check_in_date__lte=end_date) & Q(check_out_date__gte=start_date)
    ).select_related('room', 'room__room_type')
    
    # Get all rooms organized by type
    rooms = Room.objects.filter(is_active=True).select_related('room_type').order_by('room_number')
    
    context = {
        'today': today,
        'bookings': bookings,
        'rooms': rooms,
        'popup_memos': popup_memos,
        'user': request.user,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'rooms/dashboard.html', context)

@login_required
def timeline_view(request):
    # Get date range from request or default to current week
    start_date_str = request.GET.get('start_date')
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        today = timezone.now().date()
        start_date = today - timedelta(days=today.weekday())
    
    end_date = start_date + timedelta(days=13)
    
    # Get all rooms grouped by room type
    room_types = RoomType.objects.all().order_by('display_order', 'name')
    
    # Get bookings for the timeline
    bookings = Booking.objects.filter(
        Q(check_in_date__lte=end_date) & Q(check_out_date__gte=start_date)
    ).select_related('room', 'room__room_type').order_by('check_in_date')
    
    # Create timeline data grouped by room type
    timeline_data = []
    
    for room_type in room_types:
        rooms = Room.objects.filter(
            is_active=True, 
            room_type=room_type
        ).order_by('room_number')
        
        if rooms.exists():
            room_type_data = {
                'room_type': room_type,
                'rooms': []
            }
            
            for room in rooms:
                room_bookings = bookings.filter(room=room)
                room_data = {
                    'room': room,
                    'bookings': []
                }
                
                for booking in room_bookings:
                    room_data['bookings'].append({
                        'id': booking.id,
                        'guest_name': booking.guest_name,
                        'check_in': booking.check_in_date,
                        'check_out': booking.check_out_date,
                        'status': booking.status,
                        'payment_status': booking.payment_status,
                        'color': booking.get_display_color(),
                        'total_amount': booking.total_amount,
                        'paid_amount': booking.paid_amount,
                        'nights': booking.get_nights_count(),
                    })
                
                room_type_data['rooms'].append(room_data)
            
            timeline_data.append(room_type_data)
    
    # Generate date range for header
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    # Count stats
    total_bookings = bookings.count()
    total_rooms = Room.objects.filter(is_active=True).count()
    occupied_rooms = bookings.values('room').distinct().count()
    occupancy_rate = round((occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0, 1)
    total_revenue = sum(b.total_amount for b in bookings)
    
    context = {
        'timeline_data': timeline_data,
        'date_range': date_range,
        'start_date': start_date,
        'end_date': end_date,
        'prev_week': start_date - timedelta(days=14),
        'next_week': start_date + timedelta(days=14),
        'stats': {
            'total_bookings': total_bookings,
            'occupancy_rate': occupancy_rate,
            'total_revenue': total_revenue,
        }
    }
    
    return render(request, 'rooms/timeline.html', context)

@login_required
def create_booking(request):
    if request.method == 'POST':
        room_id = request.POST.get('room')
        guest_name = request.POST.get('guest_name')
        guest_contact = request.POST.get('guest_contact')
        check_in_date = datetime.strptime(request.POST.get('check_in_date'), '%Y-%m-%d').date()
        check_out_date = datetime.strptime(request.POST.get('check_out_date'), '%Y-%m-%d').date()
        notes = request.POST.get('notes', '')
        
        if check_in_date >= check_out_date:
            messages.error(request, 'Check-out date must be after check-in date')
            return render(request, 'rooms/create_booking.html', {'rooms': Room.objects.filter(is_active=True)})
        
        room = get_object_or_404(Room, id=room_id)
        
        # Calculate total amount
        total_days = (check_out_date - check_in_date).days
        total_amount = Decimal('0')
        
        current_date = check_in_date
        while current_date < check_out_date:
            daily_rate = room.get_rate_for_date(current_date)
            total_amount += daily_rate
            current_date += timedelta(days=1)
        
        booking = Booking.objects.create(
            room=room,
            guest_name=guest_name,
            guest_contact=guest_contact,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_amount=total_amount,
            notes=notes,
            created_by=request.user
        )
        
        messages.success(request, f'Booking created successfully. Total amount: ₱{total_amount}')
        return redirect('timeline')
    
    rooms = Room.objects.filter(is_active=True).select_related('room_type')
    return render(request, 'rooms/create_booking.html', {'rooms': rooms})

@login_required
@user_passes_test(is_admin_or_super)
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_payment':
            paid_amount = Decimal(request.POST.get('paid_amount', 0))
            booking.paid_amount = paid_amount
            booking.save()
            messages.success(request, 'Payment updated successfully')
        
        elif action == 'update_status':
            new_status = request.POST.get('status')
            booking.status = new_status
            booking.save()
            messages.success(request, 'Status updated successfully')
        
        elif action == 'delete' and request.user.can_delete_bookings():
            booking.delete()
            messages.success(request, 'Booking deleted successfully')
            return redirect('timeline')
        
        return redirect('booking_detail', booking_id=booking.id)
    
    context = {
        'booking': booking,
        'can_delete': request.user.can_delete_bookings(),
    }
    
    return render(request, 'rooms/booking_detail.html', context)

@login_required
@user_passes_test(is_super_user)
def manage_rates(request):
    room_types = RoomType.objects.all()
    
    if request.method == 'POST':
        room_type_id = request.POST.get('room_type_id')
        room_type = get_object_or_404(RoomType, id=room_type_id)
        
        weekday_rate = Decimal(request.POST.get('weekday_rate'))
        weekend_rate = Decimal(request.POST.get('weekend_rate'))
        
        room_type.base_weekday_rate = weekday_rate
        room_type.base_weekend_rate = weekend_rate
        room_type.save()
        
        messages.success(request, f'Rates updated for {room_type.get_name_display()}')
        return redirect('manage_rates')
    
    context = {
        'room_types': room_types,
    }
    
    return render(request, 'rooms/manage_rates.html', context)

@login_required
@user_passes_test(is_super_user)
def system_memo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_popup = request.POST.get('is_popup') == 'on'
        
        SystemMemo.objects.create(
            title=title,
            content=content,
            is_popup=is_popup,
            created_by=request.user
        )
        
        messages.success(request, 'Memo created successfully')
        return redirect('system_memo')
    
    memos = SystemMemo.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'memos': memos,
    }
    
    return render(request, 'rooms/system_memo.html', context)

@login_required
@user_passes_test(is_super_user)
def activity_log_view(request):
    log_list = ActivityLog.objects.all()
    paginator = Paginator(log_list, 25)  # Show 25 logs per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'rooms/activity_log.html', context)

@login_required
@user_passes_test(is_super_user)
def backup_management(request):
    """View for managing backups - list, export, import"""
    # Get all backups ordered by creation time
    backup_list = DataBackup.objects.all().order_by('-created_at')
    paginator = Paginator(backup_list, 20)  # Show 20 backups per page
    
    page_number = request.GET.get('page')
    backups = paginator.get_page(page_number)
    
    context = {
        'backups': backups,
        'total_backups': DataBackup.objects.count(),
        'auto_backups': DataBackup.objects.filter(backup_type='AUTO').count(),
        'manual_backups': DataBackup.objects.filter(backup_type='MANUAL').count(),
    }
    
    return render(request, 'rooms/backup_management.html', context)

@login_required
@user_passes_test(is_super_user)
def export_data(request):
    """Export current data to Excel format"""
    try:
        # Create manual backup record
        backup = create_backup_record(
            backup_type='MANUAL',
            user=request.user,
            notes=f'Manual export by {request.user.username}'
        )
        
        # Generate Excel file
        excel_buffer = export_bookings_to_excel()
        
        # Create HTTP response with Excel file
        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{backup.file_name}"'
        
        messages.success(request, f'Data exported successfully. Backup record created: {backup.file_name}')
        return response
        
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('backup_management')

@login_required
@user_passes_test(is_super_user)
def import_data(request):
    """Import data from Excel file"""
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            messages.error(request, 'No file selected for import')
            return redirect('backup_management')
        
        excel_file = request.FILES['excel_file']
        
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, 'Please select a valid Excel file (.xlsx or .xls)')
            return redirect('backup_management')
        
        try:
            # Import the data
            result = import_bookings_from_excel(excel_file, request.user)
            
            # Create import backup record
            excel_file.seek(0)  # Reset file pointer
            file_data = excel_file.read()
            
            backup = create_backup_record(
                backup_type='IMPORT',
                user=request.user,
                file_data=file_data,
                notes=f'Data import by {request.user.username}: {result["message"]}'
            )
            
            if result['success']:
                messages.success(request, result['message'])
            else:
                messages.warning(request, result['message'])
                if 'errors' in result:
                    for error in result['errors'][:5]:  # Show first 5 errors
                        messages.error(request, error)
            
            return redirect('backup_management')
            
        except Exception as e:
            messages.error(request, f'Error importing data: {str(e)}')
            return redirect('backup_management')
    
    return redirect('backup_management')

@login_required
@user_passes_test(is_super_user)
def download_backup(request, backup_id):
    """Download a specific backup file"""
    try:
        backup = get_object_or_404(DataBackup, id=backup_id)
        
        response = HttpResponse(
            backup.file_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{backup.file_name}"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error downloading backup: {str(e)}')
        return redirect('backup_management')

@login_required
@user_passes_test(is_super_user)
def delete_backup(request, backup_id):
    """Delete a specific backup"""
    if request.method == 'POST':
        try:
            backup = get_object_or_404(DataBackup, id=backup_id)
            backup_name = backup.file_name
            backup.delete()
            
            messages.success(request, f'Backup {backup_name} deleted successfully')
            
        except Exception as e:
            messages.error(request, f'Error deleting backup: {str(e)}')
    
    return redirect('backup_management')

@login_required
@user_passes_test(is_super_user)
def manual_backup(request):
    """Create a manual backup"""
    try:
        backup = create_backup_record(
            backup_type='MANUAL',
            user=request.user,
            notes=f'Manual backup created by {request.user.username}'
        )
        
        messages.success(request, f'Manual backup created successfully: {backup.file_name}')
        
    except Exception as e:
        messages.error(request, f'Error creating manual backup: {str(e)}')
    
    return redirect('backup_management')
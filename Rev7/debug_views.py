from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal
import traceback

from rooms.models import Room, RoomType, Booking, CustomUser

@login_required
def debug_create_booking(request):
    """Debug version of create booking with error handling"""
    
    if request.method == 'POST':
        try:
            # Debug: Log what we received
            print(f"POST data: {request.POST}")
            
            room_id = request.POST.get('room')
            guest_name = request.POST.get('guest_name')
            guest_contact = request.POST.get('guest_contact', '')
            check_in_date_str = request.POST.get('check_in_date')
            check_out_date_str = request.POST.get('check_out_date')
            notes = request.POST.get('notes', '')
            
            print(f"Room ID: {room_id}")
            print(f"Guest: {guest_name}")
            print(f"Dates: {check_in_date_str} to {check_out_date_str}")
            
            # Validate required fields
            if not room_id:
                messages.error(request, 'Please select a room')
                return redirect('create_booking')
                
            if not guest_name:
                messages.error(request, 'Please enter guest name')
                return redirect('create_booking')
                
            if not check_in_date_str or not check_out_date_str:
                messages.error(request, 'Please select check-in and check-out dates')
                return redirect('create_booking')
            
            # Parse dates
            try:
                check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()
                print(f"Parsed dates: {check_in_date} to {check_out_date}")
            except ValueError as e:
                messages.error(request, f'Invalid date format: {e}')
                return redirect('create_booking')
            
            if check_in_date >= check_out_date:
                messages.error(request, 'Check-out date must be after check-in date')
                return redirect('create_booking')
            
            # Get room
            try:
                room = Room.objects.get(id=room_id)
                print(f"Found room: {room.room_number} - {room.room_type.get_name_display()}")
            except Room.DoesNotExist:
                messages.error(request, 'Selected room not found')
                return redirect('create_booking')
            
            # Calculate total amount
            try:
                total_days = (check_out_date - check_in_date).days
                total_amount = Decimal('0')
                
                current_date = check_in_date
                while current_date < check_out_date:
                    daily_rate = room.get_rate_for_date(current_date)
                    total_amount += daily_rate
                    current_date += timedelta(days=1)
                
                print(f"Calculated total: ₱{total_amount} for {total_days} days")
            except Exception as e:
                messages.error(request, f'Error calculating rates: {e}')
                return redirect('create_booking')
            
            # Create booking
            try:
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
                print(f"Created booking ID: {booking.id}")
                
                messages.success(request, f'Booking created successfully! Total: ₱{total_amount}')
                return redirect('timeline')
                
            except Exception as e:
                print(f"Error creating booking: {e}")
                messages.error(request, f'Error creating booking: {e}')
                return redirect('create_booking')
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            messages.error(request, f'Unexpected error: {e}')
            return redirect('create_booking')
    
    # GET request - show form
    try:
        rooms = Room.objects.filter(is_active=True).select_related('room_type')
        room_count = rooms.count()
        room_type_count = RoomType.objects.count()
        
        print(f"Available rooms: {room_count}")
        print(f"Room types: {room_type_count}")
        
        context = {
            'rooms': rooms,
            'room_count': room_count,
            'room_type_count': room_type_count,
        }
        
        return render(request, 'rooms/create_booking.html', context)
        
    except Exception as e:
        print(f"Error loading rooms: {e}")
        messages.error(request, f'Error loading rooms: {e}')
        return render(request, 'rooms/create_booking.html', {'rooms': []})
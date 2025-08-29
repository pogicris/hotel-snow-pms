#!/usr/bin/env python3
"""
Create test data for timeline testing
"""

import os
import sys
import django
from datetime import datetime, timedelta, date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import Room, RoomType, Booking, CustomUser

def create_test_data():
    """Create test data for timeline display"""
    print("Creating test data for timeline...")
    
    try:
        # Create admin user if doesn't exist
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'user_type': 'SUPER',
                'password': 'pbkdf2_sha256$260000$dummy$dummy'
            }
        )
        
        if created:
            print("Created admin user")
        
        # Create room types if they don't exist
        room_types_data = [
            ('LOFT', 'Loft', 1),
            ('SINGLE', 'Single', 2), 
            ('DOUBLE', 'Double', 3),
            ('TRIPLE', 'Triple', 4),
        ]
        
        for code, name, order in room_types_data:
            rt, created = RoomType.objects.get_or_create(
                name=code,
                defaults={
                    'display_order': order,
                    'base_weekday_rate': 150.00,
                    'base_weekend_rate': 200.00
                }
            )
            if created:
                print(f"Created room type: {name}")
        
        # Create rooms if they don't exist
        rooms_data = [
            ('L1', 'LOFT'),
            ('L2', 'LOFT'),
            ('1A', 'SINGLE'),
            ('1B', 'SINGLE'), 
            ('1C', 'SINGLE'),
            ('1D', 'SINGLE'),
            ('D1', 'DOUBLE'),
            ('D2', 'DOUBLE'),
            ('T1', 'TRIPLE'),
        ]
        
        for room_num, room_type_code in rooms_data:
            room_type = RoomType.objects.get(name=room_type_code)
            room, created = Room.objects.get_or_create(
                room_number=room_num,
                defaults={
                    'room_type': room_type,
                    'is_active': True
                }
            )
            if created:
                print(f"Created room: {room_num}")
        
        # Create test bookings spanning multiple days
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        
        test_bookings = [
            {
                'room_number': 'L1',
                'guest': 'Sally Higgins',
                'check_in': start_date + timedelta(days=2),
                'nights': 4,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
            {
                'room_number': 'L1',
                'guest': 'Hai Jordan', 
                'check_in': start_date + timedelta(days=6),
                'nights': 7,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
            {
                'room_number': '1A',
                'guest': 'John Michael Kane',
                'check_in': start_date + timedelta(days=1),
                'nights': 3,
                'status': 'PENCIL',
                'payment': 'UNPAID'
            },
            {
                'room_number': '1B',
                'guest': 'Lars Ayn',
                'check_in': start_date,
                'nights': 2,
                'status': 'CONFIRMED',
                'payment': 'PARTIAL'
            },
            {
                'room_number': '1B',
                'guest': 'Althea Silva',
                'check_in': start_date + timedelta(days=3),
                'nights': 8,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
            {
                'room_number': 'D1',
                'guest': 'Marco Antonio',
                'check_in': start_date,
                'nights': 5,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
            {
                'room_number': 'D2',
                'guest': 'Hank Jones',
                'check_in': start_date + timedelta(days=8),
                'nights': 4,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
            {
                'room_number': 'T1',
                'guest': 'Joni Beasley',
                'check_in': start_date + timedelta(days=2),
                'nights': 6,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
        ]
        
        for booking_data in test_bookings:
            try:
                room = Room.objects.get(room_number=booking_data['room_number'])
                check_in = booking_data['check_in']
                check_out = check_in + timedelta(days=booking_data['nights'])
                
                # Check if booking already exists
                existing = Booking.objects.filter(
                    room=room,
                    guest_name=booking_data['guest'],
                    check_in_date=check_in
                ).first()
                
                if not existing:
                    total_amount = 150.00 * booking_data['nights']  # Base rate
                    paid_amount = total_amount if booking_data['payment'] == 'PAID' else (
                        total_amount * 0.5 if booking_data['payment'] == 'PARTIAL' else 0
                    )
                    
                    booking = Booking.objects.create(
                        room=room,
                        guest_name=booking_data['guest'],
                        guest_contact='+63 999 123 4567',
                        check_in_date=check_in,
                        check_out_date=check_out,
                        total_amount=total_amount,
                        paid_amount=paid_amount,
                        status=booking_data['status'],
                        payment_status=booking_data['payment'],
                        notes=f'Test booking for {booking_data["guest"]}',
                        created_by=admin_user,
                    )
                    
                    print(f"Created: {booking_data['guest']} in {room.room_number}")
                    print(f"  {check_in} to {check_out} ({booking_data['nights']} nights)")
                else:
                    print(f"Exists: {booking_data['guest']} in {room.room_number}")
            
            except Room.DoesNotExist:
                print(f"Room {booking_data['room_number']} not found, skipping booking for {booking_data['guest']}")
                continue
        
        print("\nTest data creation completed!")
        print("Visit: http://127.0.0.1:8001/timeline/ to see the timeline")
        
    except Exception as e:
        print(f"Error creating test data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_test_data()
#!/usr/bin/env python3
"""
Production initialization for Hotel PMS Rev9 on Render.com
Optimized for clean deployment with minimal setup
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import RoomType, Room, CustomUser, Booking
from django.contrib.auth.hashers import make_password
from datetime import date, timedelta
from decimal import Decimal

def setup_room_types():
    """Create room types for production"""
    print("🏨 Setting up room types...")
    
    room_types = [
        ('LOFT', 'Loft', 0, 3500, 4000),
        ('SINGLE', 'Single', 1, 2500, 3000),
        ('DOUBLE', 'Double', 2, 3000, 3500),
        ('TRIPLE', 'Triple', 3, 4000, 4500),
        ('STUDIO_A', 'Studio A', 4, 2000, 2500),
        ('STUDIO_B', 'Studio B', 5, 2200, 2700),
    ]
    
    for name, display, order, weekday, weekend in room_types:
        room_type, created = RoomType.objects.get_or_create(
            name=name,
            defaults={
                'display_order': order,
                'base_weekday_rate': Decimal(str(weekday)),
                'base_weekend_rate': Decimal(str(weekend)),
            }
        )
        if created:
            print(f"✅ {display}")

def setup_rooms():
    """Create hotel rooms"""
    print("🏠 Setting up rooms...")
    
    room_config = [
        ('LOFT', ['L1', 'L2']),
        ('SINGLE', ['1A', '1B', '1C', '1D']),
        ('DOUBLE', ['D1', 'D2']),
        ('TRIPLE', ['T1']),
        ('STUDIO_A', ['SA1', 'SA2']),
        ('STUDIO_B', ['SB1']),
    ]
    
    for room_type_name, room_numbers in room_config:
        try:
            room_type = RoomType.objects.get(name=room_type_name)
            for room_number in room_numbers:
                Room.objects.get_or_create(
                    room_number=room_number,
                    defaults={'room_type': room_type, 'is_active': True}
                )
            print(f"✅ {room_type.get_name_display()}: {', '.join(room_numbers)}")
        except RoomType.DoesNotExist:
            print(f"❌ {room_type_name} not found")

def setup_admin():
    """Create admin user"""
    print("👤 Setting up admin user...")
    
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@hotel.com')
    password = os.environ.get('ADMIN_PASSWORD', 'HotelAdmin2024!')
    
    user, created = CustomUser.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'password': make_password(password),
            'first_name': 'Hotel',
            'last_name': 'Administrator',
            'user_type': 'SUPER',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    if created:
        print(f"✅ Admin user created: {username}")
    else:
        print(f"✅ Admin user exists: {username}")

def create_demo_data():
    """Create minimal demo bookings for timeline"""
    print("📅 Creating demo bookings...")
    
    admin = CustomUser.objects.filter(user_type='SUPER').first()
    rooms = Room.objects.all()[:4]
    
    if not admin or not rooms:
        print("❌ Missing admin or rooms for demo data")
        return
    
    guests = ["Sally Higgins", "Hal Jordan", "John Kane", "Lars Anderson"]
    start = date.today()
    
    demo_bookings = [
        (rooms[0], guests[0], start + timedelta(days=1), start + timedelta(days=5), 'PAID'),
        (rooms[1], guests[1], start + timedelta(days=2), start + timedelta(days=7), 'PENCIL'),
        (rooms[2], guests[2], start + timedelta(days=3), start + timedelta(days=6), 'PARTIAL'),
        (rooms[3], guests[3], start + timedelta(days=5), start + timedelta(days=9), 'PAID'),
    ]
    
    for room, guest, check_in, check_out, payment_status in demo_bookings:
        if Booking.objects.filter(room=room, guest_name=guest).exists():
            continue
            
        days = (check_out - check_in).days
        total = room.get_rate_for_date(check_in) * days
        paid = total if payment_status == 'PAID' else (total * Decimal('0.5') if payment_status == 'PARTIAL' else Decimal('0'))
        
        Booking.objects.create(
            room=room,
            guest_name=guest,
            guest_contact='+63 999 123 4567',
            check_in_date=check_in,
            check_out_date=check_out,
            total_amount=total,
            paid_amount=paid,
            status='CONFIRMED' if payment_status != 'PENCIL' else 'PENCIL',
            payment_status=payment_status,
            notes='Demo booking for Rev9',
            created_by=admin,
        )
    
    print(f"✅ Created {len(demo_bookings)} demo bookings")

def main():
    """Initialize production environment"""
    print("=" * 50)
    print("🚀 Hotel PMS Rev9 - Production Setup")
    print("=" * 50)
    
    try:
        setup_room_types()
        setup_rooms()
        setup_admin()
        
        # Only create demo data in development
        if not os.environ.get('PRODUCTION', False):
            create_demo_data()
        
        print("\n" + "=" * 50)
        print("✅ Rev9 production setup complete!")
        print("🌐 Ready for Render.com deployment")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
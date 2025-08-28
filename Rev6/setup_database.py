#!/usr/bin/env python
import os
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import RoomType, Room, CustomUser
from decimal import Decimal

def setup_database():
    print("🔄 Running migrations...")
    call_command('migrate', verbosity=2)
    
    print("🏨 Setting up room types...")
    
    # Room type configurations
    room_configs = [
        {
            'type': 'STUDIO_A',
            'description': 'Studio A',
            'rooms': ['101', '102', '103', '104', '105', '106', '107', '110', '111', '112', '113', '114', '115', '116', '117'],
            'weekday_rate': Decimal('2000.00'),
            'weekend_rate': Decimal('2500.00')
        },
        {
            'type': 'STUDIO_A_PROMO',
            'description': 'Studio A Promo',
            'rooms': ['108', '109', '118', '119'],
            'weekday_rate': Decimal('1800.00'),
            'weekend_rate': Decimal('2200.00')
        },
        {
            'type': 'STUDIO_B',
            'description': 'Studio B',
            'rooms': ['201', '203', '205', '207', '209', '211', '212'],
            'weekday_rate': Decimal('2200.00'),
            'weekend_rate': Decimal('2700.00')
        },
        {
            'type': 'STUDIO_DELUXE',
            'description': 'Studio Deluxe',
            'rooms': ['202', '204', '206', '208', '210'],
            'weekday_rate': Decimal('2800.00'),
            'weekend_rate': Decimal('3300.00')
        },
        {
            'type': 'FAMILY_NO_BALCONY',
            'description': 'Family Room w/o Balcony',
            'rooms': ['216', '214'],
            'weekday_rate': Decimal('3500.00'),
            'weekend_rate': Decimal('4000.00')
        },
        {
            'type': 'FAMILY_WITH_BALCONY',
            'description': 'Family Room w/ Balcony',
            'rooms': ['213', '215'],
            'weekday_rate': Decimal('4000.00'),
            'weekend_rate': Decimal('4500.00')
        },
        {
            'type': 'PENTHOUSE',
            'description': 'Penthouse',
            'rooms': ['301', '302'],
            'weekday_rate': Decimal('6000.00'),
            'weekend_rate': Decimal('7000.00')
        },
        {
            'type': 'MODULE_HOUSE',
            'description': 'Module House',
            'rooms': ['401', '402'],
            'weekday_rate': Decimal('5000.00'),
            'weekend_rate': Decimal('6000.00')
        },
        {
            'type': 'KTV',
            'description': 'KTV Room',
            'rooms': ['501', '502', '503', '504'],
            'weekday_rate': Decimal('1500.00'),
            'weekend_rate': Decimal('2000.00')
        }
    ]
    
    total_rooms = 0
    for config in room_configs:
        # Create or get room type
        room_type, created = RoomType.objects.get_or_create(
            name=config['type'],
            defaults={
                'description': config['description'],
                'base_weekday_rate': config['weekday_rate'],
                'base_weekend_rate': config['weekend_rate']
            }
        )
        
        if created:
            print(f"✅ Created room type: {config['description']}")
        else:
            print(f"♻️  Room type exists: {config['description']}")
            # Update rates if they exist
            room_type.base_weekday_rate = config['weekday_rate']
            room_type.base_weekend_rate = config['weekend_rate']
            room_type.save()
        
        # Create rooms
        for room_number in config['rooms']:
            room, room_created = Room.objects.get_or_create(
                room_number=room_number,
                defaults={'room_type': room_type}
            )
            
            if room_created:
                print(f"  ✅ Created room: {room_number}")
                total_rooms += 1
            else:
                print(f"  ♻️  Room exists: {room_number}")
    
    print(f"🏨 Total rooms in system: {Room.objects.count()}")
    print(f"🏷️  Total room types: {RoomType.objects.count()}")
    
    print("👤 Setting up users...")
    
    # Create users
    users_to_create = [
        {
            'username': 'superadmin',
            'password': 'snow2024!',
            'email': 'super@hotelsnow.com',
            'user_type': 'SUPER',
            'is_superuser': True,
            'is_staff': True,
            'first_name': 'Super',
            'last_name': 'Admin'
        },
        {
            'username': 'admin',
            'password': 'admin2024!',
            'email': 'admin@hotelsnow.com',
            'user_type': 'ADMIN',
            'is_staff': True,
            'first_name': 'Hotel',
            'last_name': 'Admin'
        },
        {
            'username': 'frontdesk',
            'password': 'front2024!',
            'email': 'frontdesk@hotelsnow.com',
            'user_type': 'MEMBER',
            'first_name': 'Front',
            'last_name': 'Desk'
        }
    ]

    for user_data in users_to_create:
        username = user_data['username']
        if not CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email'],
                user_type=user_data['user_type'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            if user_data.get('is_superuser'):
                user.is_superuser = True
                user.is_staff = True
                user.save()
            elif user_data.get('is_staff'):
                user.is_staff = True
                user.save()
            
            print(f"✅ Created user: {username} ({user_data['user_type']})")
        else:
            print(f"♻️  User exists: {username}")

    print("🎉 Database setup completed successfully!")
    print(f"📊 Final counts:")
    print(f"   - Room Types: {RoomType.objects.count()}")
    print(f"   - Rooms: {Room.objects.count()}")
    print(f"   - Users: {CustomUser.objects.count()}")

if __name__ == '__main__':
    setup_database()
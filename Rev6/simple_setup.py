import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import RoomType, Room, CustomUser
from decimal import Decimal

# Simple room setup
rooms_data = {
    'STUDIO_A': {
        'name': 'Studio A',
        'weekday': 2000,
        'weekend': 2500,
        'rooms': ['101', '102', '103', '104', '105', '106', '107', '110', '111', '112', '113', '114', '115', '116', '117']
    },
    'STUDIO_A_PROMO': {
        'name': 'Studio A Promo', 
        'weekday': 1800,
        'weekend': 2200,
        'rooms': ['108', '109', '118', '119']
    },
    'STUDIO_B': {
        'name': 'Studio B',
        'weekday': 2200,
        'weekend': 2700, 
        'rooms': ['201', '203', '205', '207', '209', '211', '212']
    },
    'STUDIO_DELUXE': {
        'name': 'Studio Deluxe',
        'weekday': 2800,
        'weekend': 3300,
        'rooms': ['202', '204', '206', '208', '210']
    },
    'FAMILY_NO_BALCONY': {
        'name': 'Family Room w/o Balcony',
        'weekday': 3500,
        'weekend': 4000,
        'rooms': ['216', '214']
    },
    'FAMILY_WITH_BALCONY': {
        'name': 'Family Room w/ Balcony', 
        'weekday': 4000,
        'weekend': 4500,
        'rooms': ['213', '215']
    },
    'PENTHOUSE': {
        'name': 'Penthouse',
        'weekday': 6000,
        'weekend': 7000,
        'rooms': ['301', '302']
    },
    'MODULE_HOUSE': {
        'name': 'Module House',
        'weekday': 5000,
        'weekend': 6000,
        'rooms': ['401', '402']
    },
    'KTV': {
        'name': 'KTV Room',
        'weekday': 1500,
        'weekend': 2000,
        'rooms': ['501', '502', '503', '504']
    }
}

print("Setting up rooms...")
for room_type_code, data in rooms_data.items():
    # Create room type
    room_type, created = RoomType.objects.get_or_create(
        name=room_type_code,
        defaults={
            'description': data['name'],
            'base_weekday_rate': Decimal(str(data['weekday'])),
            'base_weekend_rate': Decimal(str(data['weekend']))
        }
    )
    if created:
        print(f"Created room type: {data['name']}")
    
    # Create rooms
    for room_num in data['rooms']:
        room, created = Room.objects.get_or_create(
            room_number=room_num,
            defaults={'room_type': room_type, 'is_active': True}
        )
        if created:
            print(f"Created room: {room_num}")

# Create users
print("Setting up users...")
if not CustomUser.objects.filter(username='superadmin').exists():
    user = CustomUser.objects.create_user('superadmin', 'super@hotel.com', 'snow2024!')
    user.user_type = 'SUPER'
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Created superadmin")

if not CustomUser.objects.filter(username='admin').exists():
    user = CustomUser.objects.create_user('admin', 'admin@hotel.com', 'admin2024!')
    user.user_type = 'ADMIN'
    user.is_staff = True
    user.save()
    print("Created admin")

if not CustomUser.objects.filter(username='frontdesk').exists():
    user = CustomUser.objects.create_user('frontdesk', 'front@hotel.com', 'front2024!')
    user.user_type = 'MEMBER'
    user.save()
    print("Created frontdesk")

print(f"Total rooms: {Room.objects.count()}")
print(f"Total room types: {RoomType.objects.count()}")
print(f"Total users: {CustomUser.objects.count()}")
print("Setup complete!")
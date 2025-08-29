import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import RoomType, Room, CustomUser
from decimal import Decimal

print("Starting room setup...")

# Simple room setup with just 3 room types for testing
rooms_data = {
    'STUDIO_A': {
        'name': 'Studio A',
        'weekday': 2000,
        'weekend': 2500,
        'rooms': ['101', '102', '103', '104', '105']
    },
    'STUDIO_A_PROMO': {
        'name': 'Studio A Promo', 
        'weekday': 1800,
        'weekend': 2200,
        'rooms': ['108', '109']
    },
    'STUDIO_B': {
        'name': 'Studio B',
        'weekday': 2200,
        'weekend': 2700, 
        'rooms': ['201', '203', '205']
    }
}

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
    else:
        print(f"Room type exists: {data['name']}")
    
    # Create rooms
    for room_num in data['rooms']:
        room, created = Room.objects.get_or_create(
            room_number=room_num,
            defaults={'room_type': room_type, 'is_active': True}
        )
        if created:
            print(f"Created room: {room_num}")

# Create superuser
if not CustomUser.objects.filter(username='superadmin').exists():
    user = CustomUser.objects.create_user('superadmin', 'super@hotel.com', 'snow2024!')
    user.user_type = 'SUPER'
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("Created superadmin user")
else:
    print("Superadmin already exists")

print(f"Setup complete! Rooms: {Room.objects.count()}, Room Types: {RoomType.objects.count()}")
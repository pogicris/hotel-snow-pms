from django.core.management.base import BaseCommand
from rooms.models import RoomType, Room
from decimal import Decimal

class Command(BaseCommand):
    help = 'Setup initial room types and rooms for Hotel Snow PMS'

    def handle(self, *args, **options):
        room_configurations = [
            {
                'type': 'STUDIO_A',
                'name': 'Studio A',
                'rooms': ['101', '102', '103', '104', '105', '106', '107', '110', '111', '112', '113', '114', '115', '116', '117'],
                'weekday_rate': Decimal('2000.00'),
                'weekend_rate': Decimal('2500.00'),
                'display_order': 10
            },
            {
                'type': 'STUDIO_A_PROMO',
                'name': 'Studio A Promo',
                'rooms': ['108', '109', '118', '119'],
                'weekday_rate': Decimal('1800.00'),
                'weekend_rate': Decimal('2200.00'),
                'display_order': 20
            },
            {
                'type': 'STUDIO_B',
                'name': 'Studio B',
                'rooms': ['201', '203', '205', '207', '209', '211', '212'],
                'weekday_rate': Decimal('2200.00'),
                'weekend_rate': Decimal('2700.00'),
                'display_order': 30
            },
            {
                'type': 'STUDIO_DELUXE',
                'name': 'Studio Deluxe',
                'rooms': ['202', '204', '206', '208', '210'],
                'weekday_rate': Decimal('2800.00'),
                'weekend_rate': Decimal('3300.00'),
                'display_order': 40
            },
            {
                'type': 'FAMILY_NO_BALCONY',
                'name': 'Family Room w/o Balcony',
                'rooms': ['216', '214'],
                'weekday_rate': Decimal('3500.00'),
                'weekend_rate': Decimal('4000.00'),
                'display_order': 50
            },
            {
                'type': 'FAMILY_WITH_BALCONY',
                'name': 'Family Room w/ Balcony',
                'rooms': ['213', '215'],
                'weekday_rate': Decimal('4000.00'),
                'weekend_rate': Decimal('4500.00'),
                'display_order': 60
            },
            {
                'type': 'PENTHOUSE',
                'name': 'Penthouse',
                'rooms': ['301', '302'],
                'weekday_rate': Decimal('6000.00'),
                'weekend_rate': Decimal('7000.00'),
                'display_order': 70
            },
            {
                'type': 'MODULE_HOUSE',
                'name': 'Module House',
                'rooms': ['401', '402'],
                'weekday_rate': Decimal('5000.00'),
                'weekend_rate': Decimal('6000.00'),
                'display_order': 80
            },
            {
                'type': 'KTV',
                'name': 'KTV Room',
                'rooms': ['501', '502', '503', '504'],
                'weekday_rate': Decimal('1500.00'),
                'weekend_rate': Decimal('2000.00'),
                'display_order': 90
            }
        ]

        self.stdout.write('Updating room types and rooms...')
        
        for config in room_configurations:
            room_type, created = RoomType.objects.update_or_create(
                name=config['type'],
                defaults={
                    'description': config['name'],
                    'base_weekday_rate': config['weekday_rate'],
                    'base_weekend_rate': config['weekend_rate'],
                    'display_order': config['display_order']
                }
            )
            
            if created:
                self.stdout.write(f'Created room type: {config["name"]}')
            else:
                self.stdout.write(f'Updated room type: {config["name"]}')
            
            for room_number in config['rooms']:
                room, room_created = Room.objects.get_or_create(
                    room_number=room_number,
                    defaults={'room_type': room_type}
                )
                
                if room_created:
                    self.stdout.write(f'  Created room: {room_number}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully updated all rooms and room types!')
        )
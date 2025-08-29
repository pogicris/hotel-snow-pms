#!/usr/bin/env python3
"""
Update room type display order to match business requirements
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import RoomType

def update_room_order():
    """Update room type display order"""
    print("Updating room type display order...")
    
    # Business requirement order:
    # Studio A, Studio A Promo, B, Deluxe, Family, Penthouse, Module House, KTV
    order_mapping = {
        'STUDIO_A': 1,
        'STUDIO_A_PROMO': 2,
        'STUDIO_B': 3,
        'STUDIO_DELUXE': 4,
        'FAMILY_NO_BALCONY': 5,
        'FAMILY_WITH_BALCONY': 6,
        'PENTHOUSE': 7,
        'MODULE_HOUSE': 8,
        'KTV': 9,
        # Legacy types (if they exist)
        'LOFT': 10,
        'SINGLE': 11,
        'DOUBLE': 12,
        'TRIPLE': 13,
    }
    
    try:
        updated_count = 0
        for room_type_code, display_order in order_mapping.items():
            try:
                room_type = RoomType.objects.get(name=room_type_code)
                room_type.display_order = display_order
                room_type.save()
                print(f"Updated {room_type.get_name_display()}: order {display_order}")
                updated_count += 1
            except RoomType.DoesNotExist:
                print(f"Room type {room_type_code} not found, skipping...")
                continue
        
        print(f"\nSuccessfully updated {updated_count} room types!")
        print("Timeline will now show room types in the correct business order.")
        
    except Exception as e:
        print(f"Error updating room order: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    update_room_order()
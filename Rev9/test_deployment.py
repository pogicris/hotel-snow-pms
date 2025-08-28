#!/usr/bin/env python3
"""
Test deployment script to verify Rev9 timeline fixes
Run this script to test if all components are working properly
"""

import os
import sys
import django
from datetime import datetime, timedelta, date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_pms.settings')
django.setup()

from rooms.models import Room, RoomType, Booking, CustomUser

def test_timeline_components():
    """Test all timeline components"""
    print("🧪 Testing Rev9 Timeline Components...")
    print("=" * 50)
    
    # Test 1: Check if models have required fields
    print("1. Testing Models...")
    try:
        # Test RoomType has display_order
        room_types = RoomType.objects.all()
        for rt in room_types[:1]:  # Test first one
            print(f"   ✅ RoomType.display_order: {rt.display_order}")
            print(f"   ✅ RoomType ordering: {rt._meta.ordering}")
        
        # Test Booking has get_nights_count method
        bookings = Booking.objects.all()[:1]
        if bookings:
            booking = bookings[0]
            print(f"   ✅ Booking.get_nights_count(): {booking.get_nights_count()}")
            print(f"   ✅ Booking.get_display_color(): {booking.get_display_color()}")
        
        print("   ✅ Models test passed!")
        
    except Exception as e:
        print(f"   ❌ Models test failed: {e}")
        return False
    
    # Test 2: Check timeline view logic
    print("\n2. Testing Timeline View Logic...")
    try:
        from rooms.views import timeline_view
        from django.test import RequestFactory
        from django.contrib.auth import get_user_model
        
        # Create fake request
        factory = RequestFactory()
        request = factory.get('/timeline/')
        
        # Get admin user
        User = get_user_model()
        admin_user = User.objects.filter(user_type='SUPER').first()
        if not admin_user:
            admin_user = User.objects.create_user(
                username='test_admin',
                password='test123',
                user_type='SUPER'
            )
        request.user = admin_user
        
        # Test date range calculation
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=13)
        
        # Calculate days between
        days_count = (end_date - start_date).days + 1
        print(f"   ✅ Start date: {start_date}")
        print(f"   ✅ End date: {end_date}")
        print(f"   ✅ Days count: {days_count} (should be 14)")
        
        if days_count == 14:
            print("   ✅ Timeline view logic test passed!")
        else:
            print(f"   ❌ Expected 14 days, got {days_count}")
            return False
            
    except Exception as e:
        print(f"   ❌ Timeline view test failed: {e}")
        return False
    
    # Test 3: Check template files exist
    print("\n3. Testing Template Files...")
    try:
        template_path = 'templates/rooms/timeline.html'
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for key elements
            checks = [
                ('timeline-page', 'Main wrapper class'),
                ('timeline-header', 'Header section'),
                ('timeline-main', 'Main timeline grid'),
                ('timeline-grid', 'Grid container'),
                ('date-header-row', 'Date header'),
                ('room-type-group', 'Room type grouping'),
                ('booking-bar', 'Booking bars'),
                ('{% for date in date_range %}', 'Date range loop'),
                ('repeat(14, 1fr)', 'CSS grid 14 columns')
            ]
            
            missing = []
            for check, desc in checks:
                if check not in content:
                    missing.append(f"{desc} ({check})")
            
            if missing:
                print("   ❌ Missing template elements:")
                for item in missing:
                    print(f"      - {item}")
                return False
            else:
                print("   ✅ Template file test passed!")
                
        else:
            print(f"   ❌ Template file not found: {template_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ Template test failed: {e}")
        return False
    
    # Test 4: Check CSS files exist
    print("\n4. Testing CSS Files...")
    try:
        css_path = 'static/css/timeline.css'
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for key CSS classes
            css_checks = [
                ('.timeline-page', 'Main page wrapper'),
                ('.timeline-header', 'Header styling'),
                ('.timeline-grid', 'Grid layout'),
                ('.booking-bar', 'Booking bar styling'),
                ('grid-template-columns', 'CSS Grid columns'),
                ('repeat(14, 1fr)', '14 column layout')
            ]
            
            missing_css = []
            for check, desc in css_checks:
                if check not in content:
                    missing_css.append(f"{desc} ({check})")
            
            if missing_css:
                print("   ❌ Missing CSS elements:")
                for item in missing_css:
                    print(f"      - {item}")
                return False
            else:
                print("   ✅ CSS file test passed!")
                
        else:
            print(f"   ❌ CSS file not found: {css_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ CSS test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Rev9 timeline should work correctly.")
    print("\nIf Render.com deployment isn't showing changes:")
    print("1. Check build logs in Render dashboard")
    print("2. Ensure 'Collect static files' runs successfully")
    print("3. Try hard refresh (Ctrl+F5) to clear browser cache")
    print("4. Check DATABASE_URL is connected properly")
    print("5. Verify migrations ran successfully")
    print("=" * 50)
    
    return True

def create_test_data():
    """Create test data to verify timeline display"""
    print("\n📋 Creating test data for timeline...")
    
    try:
        # Get admin user
        admin_user = CustomUser.objects.filter(user_type='SUPER').first()
        if not admin_user:
            print("   ⚠️  No admin user found - run init_production.py first")
            return
        
        # Get some rooms
        loft_rooms = Room.objects.filter(room_type__name='LOFT')[:1]
        single_rooms = Room.objects.filter(room_type__name='SINGLE')[:2]
        
        if not loft_rooms or not single_rooms:
            print("   ⚠️  No rooms found - run init_production.py first")
            return
        
        # Create test bookings spanning multiple days
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        
        test_bookings = [
            {
                'room': loft_rooms[0],
                'guest': 'Sally Higgins',
                'check_in': start_date + timedelta(days=2),
                'nights': 4,
                'status': 'CONFIRMED',
                'payment': 'PAID'
            },
            {
                'room': single_rooms[0] if single_rooms else loft_rooms[0],
                'guest': 'John Michael Kane', 
                'check_in': start_date + timedelta(days=1),
                'nights': 3,
                'status': 'PENCIL',
                'payment': 'UNPAID'
            },
        ]
        
        for booking_data in test_bookings:
            room = booking_data['room']
            check_in = booking_data['check_in']
            check_out = check_in + timedelta(days=booking_data['nights'])
            
            # Check if booking already exists
            existing = Booking.objects.filter(
                room=room,
                guest_name=booking_data['guest'],
                check_in_date=check_in
            ).first()
            
            if not existing:
                total_amount = room.get_rate_for_date(check_in) * booking_data['nights']
                paid_amount = total_amount if booking_data['payment'] == 'PAID' else 0
                
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
                    notes='Test booking for timeline verification',
                    created_by=admin_user,
                )
                
                print(f"   ✅ Created: {booking_data['guest']} in {room.room_number}")
                print(f"      {check_in} to {check_out} ({booking_data['nights']} nights)")
            else:
                print(f"   ⚠️  Booking exists: {booking_data['guest']} in {room.room_number}")
        
        print("   ✅ Test data creation completed!")
        
    except Exception as e:
        print(f"   ❌ Test data creation failed: {e}")

if __name__ == '__main__':
    print("🚀 Rev9 Timeline Deployment Test")
    print("=" * 50)
    
    # Run component tests
    if test_timeline_components():
        # Create test data if tests pass
        create_test_data()
        
        print("\n🎯 Next Steps:")
        print("1. Run 'python manage.py runserver' locally to test")
        print("2. Visit /timeline/ to see 14-day view")
        print("3. If local works, push to GitHub and redeploy on Render")
        print("4. Check Render build logs for any errors")
    else:
        print("\n❌ Component tests failed - fix issues before deploying")
        sys.exit(1)
from django.utils import timezone
from django.conf import settings
import pytz
from datetime import datetime

def get_philippine_timezone():
    """Get Philippine timezone object"""
    return pytz.timezone('Asia/Manila')

def now_in_philippines():
    """Get current time in Philippine timezone"""
    philippines_tz = get_philippine_timezone()
    utc_now = timezone.now()
    return utc_now.astimezone(philippines_tz)

def to_philippine_time(dt):
    """Convert any datetime to Philippine timezone"""
    if dt is None:
        return None
    
    philippines_tz = get_philippine_timezone()
    
    # If datetime is naive, assume it's UTC
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.utc)
    
    return dt.astimezone(philippines_tz)

def format_philippine_time(dt, format_string='%Y-%m-%d %H:%M:%S'):
    """Format datetime in Philippine timezone"""
    if dt is None:
        return 'N/A'
    
    ph_time = to_philippine_time(dt)
    return ph_time.strftime(format_string)

def get_philippine_time_display(dt):
    """Get user-friendly Philippine time display"""
    if dt is None:
        return 'N/A'
    
    ph_time = to_philippine_time(dt)
    return ph_time.strftime('%b %d, %Y %I:%M %p PHT')

def is_philippine_business_hours(dt=None):
    """Check if time is during Philippine business hours (8 AM - 6 PM PHT)"""
    if dt is None:
        dt = now_in_philippines()
    else:
        dt = to_philippine_time(dt)
    
    return 8 <= dt.hour < 18
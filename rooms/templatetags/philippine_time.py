from django import template
from django.utils.safestring import mark_safe
from rooms.timezone_utils import to_philippine_time, format_philippine_time, get_philippine_time_display

register = template.Library()

@register.filter
def ph_time(value, format_string='%b %d, %Y %I:%M %p'):
    """Convert datetime to Philippine time and format it"""
    if value is None:
        return 'N/A'
    
    try:
        ph_time = to_philippine_time(value)
        formatted_time = ph_time.strftime(format_string)
        return mark_safe(f'{formatted_time} <small class="text-muted">PHT</small>')
    except:
        return str(value)

@register.filter 
def ph_date(value):
    """Convert datetime to Philippine date only"""
    if value is None:
        return 'N/A'
    
    try:
        ph_time = to_philippine_time(value)
        return ph_time.strftime('%b %d, %Y')
    except:
        return str(value)

@register.filter
def ph_time_short(value):
    """Convert datetime to Philippine time (short format)"""
    if value is None:
        return 'N/A'
    
    try:
        ph_time = to_philippine_time(value)
        formatted_time = ph_time.strftime('%m/%d %I:%M %p')
        return mark_safe(f'{formatted_time} <small class="text-muted">PHT</small>')
    except:
        return str(value)

@register.simple_tag
def current_ph_time():
    """Get current Philippine time"""
    from rooms.timezone_utils import now_in_philippines
    ph_now = now_in_philippines()
    return mark_safe(f'{ph_now.strftime("%b %d, %Y %I:%M %p")} <small class="text-muted">PHT</small>')

@register.filter
def time_ago_ph(value):
    """Show how long ago something happened in Philippine context"""
    if value is None:
        return 'N/A'
    
    try:
        from rooms.timezone_utils import now_in_philippines
        ph_now = now_in_philippines()
        ph_time = to_philippine_time(value)
        
        diff = ph_now - ph_time
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return str(value)
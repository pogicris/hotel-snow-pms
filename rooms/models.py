from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import holidays

class RoomType(models.Model):
    ROOM_TYPE_CHOICES = [
        ('STUDIO_A', 'Studio A'),
        ('STUDIO_A_PROMO', 'Studio A Promo'),
        ('STUDIO_B', 'Studio B'),
        ('STUDIO_DELUXE', 'Studio Deluxe'),
        ('FAMILY_NO_BALCONY', 'Family Room w/o Balcony'),
        ('FAMILY_WITH_BALCONY', 'Family Room w/ Balcony'),
        ('PENTHOUSE', 'Penthouse'),
        ('MODULE_HOUSE', 'Module House'),
        ('KTV', 'KTV Room'),
        ('LOFT', 'Loft'),
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('TRIPLE', 'Triple'),
    ]
    
    name = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    base_weekday_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_weekend_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.get_name_display()

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['room_number']
    
    def __str__(self):
        return f"{self.room_number} - {self.room_type}"
    
    def get_rate_for_date(self, date):
        ph_holidays = holidays.Philippines()
        
        is_weekend = date.weekday() >= 4  # Friday = 4, Saturday = 5
        is_holiday = date in ph_holidays
        
        if is_weekend or is_holiday:
            return self.room_type.base_weekend_rate
        return self.room_type.base_weekday_rate

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
        ('SUPER', 'Super User'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='MEMBER')
    
    def can_view_logs(self):
        return self.user_type == 'ADMIN' or self.user_type == 'SUPER'
    
    def can_manage_rates(self):
        return self.user_type == 'SUPER'
    
    def can_delete_bookings(self):
        return self.user_type == 'ADMIN' or self.user_type == 'SUPER'

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENCIL', 'Pencil Booked'),
        ('CONFIRMED', 'Confirmed'),
        ('CHECKED_IN', 'Checked In'),
        ('NO_SHOW', 'No Show'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial Payment'),
        ('PAID', 'Fully Paid'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    guest_contact = models.CharField(max_length=50, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENCIL')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.check_in_date >= self.check_out_date:
            raise ValidationError('Check-out date must be after check-in date')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        self.update_payment_status()
        super().save(*args, **kwargs)
    
    def update_payment_status(self):
        if self.paid_amount >= self.total_amount:
            self.payment_status = 'PAID'
        elif self.paid_amount > 0:
            self.payment_status = 'PARTIAL'
        else:
            self.payment_status = 'UNPAID'
    
    def get_display_color(self):
        if self.status == 'NO_SHOW':
            return 'red'
        elif self.payment_status == 'PAID':
            return 'blue'
        elif self.payment_status == 'PARTIAL':
            return 'violet'
        elif self.status == 'PENCIL':
            return 'green'
        return 'gray'
    
    def get_nights_count(self):
        return (self.check_out_date - self.check_in_date).days
    
    @classmethod
    def check_room_availability(cls, room, check_in_date, check_out_date, exclude_booking_id=None):
        """
        Check if a room is available for the given date range.
        Returns a list of conflicting bookings if any exist.
        """
        # Query for overlapping bookings
        overlapping_bookings = cls.objects.filter(
            room=room,
            status__in=['PENCIL', 'CONFIRMED', 'CHECKED_IN']  # Only active bookings
        ).filter(
            # Check for date overlap: new booking overlaps with existing if:
            # (new_check_in < existing_check_out) AND (new_check_out > existing_check_in)
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        )
        
        # Exclude current booking if we're editing
        if exclude_booking_id:
            overlapping_bookings = overlapping_bookings.exclude(id=exclude_booking_id)
        
        return list(overlapping_bookings)
    
    def __str__(self):
        return f"{self.guest_name} - {self.room} ({self.check_in_date} to {self.check_out_date})"
    
    class Meta:
        ordering = ['check_in_date', 'room__room_number']

class SystemMemo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_popup = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

class DataBackup(models.Model):
    BACKUP_TYPE_CHOICES = [
        ('AUTO', 'Automatic Backup'),
        ('MANUAL', 'Manual Backup'),
        ('IMPORT', 'Data Import'),
    ]
    
    backup_type = models.CharField(max_length=10, choices=BACKUP_TYPE_CHOICES, default='AUTO')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    file_name = models.CharField(max_length=255)
    file_data = models.BinaryField()  # Store Excel file data
    booking_count = models.IntegerField(default=0)
    room_count = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_backup_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['backup_type', '-created_at']),
            models.Index(fields=['-created_at']),
        ]
    
    def get_file_size(self):
        """Get file size in KB"""
        if self.file_data:
            return len(self.file_data) / 1024
        return 0
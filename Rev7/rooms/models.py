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
    ]
    
    name = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    base_weekday_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_weekend_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
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
            return 'green'
        elif self.payment_status == 'PARTIAL':
            return 'violet'
        elif self.status == 'PENCIL':
            return 'yellow'
        return 'gray'
    
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

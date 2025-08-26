from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RoomType, Room, CustomUser, Booking, SystemMemo

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'base_weekday_rate', 'base_weekend_rate']
    list_filter = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_active']
    list_filter = ['room_type', 'is_active']
    search_fields = ['room_number']
    ordering = ['room_number']

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )
    list_display = UserAdmin.list_display + ('user_type',)
    list_filter = UserAdmin.list_filter + ('user_type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'check_in_date', 'check_out_date', 'status', 'payment_status', 'total_amount', 'paid_amount']
    list_filter = ['status', 'payment_status', 'check_in_date', 'room__room_type']
    search_fields = ['guest_name', 'guest_contact', 'room__room_number']
    date_hierarchy = 'check_in_date'
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(SystemMemo)
class SystemMemoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_popup', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_popup', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_by', 'created_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

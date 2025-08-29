from django.urls import path
from . import views
import debug_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('create-booking/', debug_views.debug_create_booking, name='create_booking'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('manage-rates/', views.manage_rates, name='manage_rates'),
    path('system-memo/', views.system_memo, name='system_memo'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('timeline/', views.timeline_view, name='timeline'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('manage-rates/', views.manage_rates, name='manage_rates'),
    path('system-memo/', views.system_memo, name='system_memo'),
    path('activity-log/', views.activity_log_view, name='activity_log'),
]
"""
Маршрутизация URL приложения club_booking.
Вариант 4: Бронирование дорожек в боулинге и столов в бильярдном клубе.
Все маршруты строго именованы (name=...), ссылки в шаблонах через {% url %}.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Публичный пользовательский портал
    path('', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('map/', views.hall_map_view, name='hall_map'),
    path('booking/', views.booking_wizard_view, name='booking_wizard'),
    path('booking/create/', views.booking_create_view, name='booking_create'),
    path('booking/<int:resource_id>/', views.booking_wizard_view, name='booking_wizard_resource'),
    path('booking/success/<int:booking_id>/', views.booking_success_view, name='booking_success'),
    path('payment/<int:booking_id>/', views.payment_process_view, name='payment_process'),
    path('check-booking/', views.check_booking_view, name='check_booking'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('profile/', views.profile_view, name='profile'),
    path('bar/', views.bar_menu_view, name='bar_menu'),
    path('about/', views.about_view, name='about'),

    # АРМ Персонала
    path('staff/dashboard/', views.staff_dashboard_view, name='staff_dashboard'),
    path('staff/booking/<int:booking_id>/status/', views.staff_change_status_view, name='staff_change_status'),

    # REST / AJAX API
    path('api/calculate-price/', views.api_calculate_price, name='api_calculate_price'),
    path('api/available-resources/', views.api_available_resources, name='api_available_resources'),
    path('api/check-card/', views.api_check_card, name='api_check_card'),
    path('api/bar-items/', views.api_bar_items, name='api_bar_items'),
]

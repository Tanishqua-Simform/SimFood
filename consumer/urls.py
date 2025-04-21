'''
Consumer/Urls.py - It contains url endpoints for -
1. Retrieving Menu (Get and Put)
2. Payment (Get and Put)
3. Scanner (Get)
'''
from django.urls import path
from .views import ViewMenuChangeEatPreferenceDaily, payment_process, came_to_eat_attendance_scanner

urlpatterns = [
    path('menu/', ViewMenuChangeEatPreferenceDaily.as_view(), name="view_menu_change_preference"),
    path('payment/', payment_process, name="payment_process"),
    path('scanner/', came_to_eat_attendance_scanner, name="scanner")
]

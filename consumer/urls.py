from django.urls import path
from .views import ViewMenuChangeEatPreferenceDaily, payment_process

urlpatterns = [
    path('menu/', ViewMenuChangeEatPreferenceDaily.as_view(), name="view_menu_change_preference"),
    path('payment/', payment_process, name="payment_process")
]

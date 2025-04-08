from django.urls import path
from .views import ViewMenuChangeEatPreferenceDaily

urlpatterns = [
    path('menu/', ViewMenuChangeEatPreferenceDaily.as_view(), name="view_menu_change_preference")
]

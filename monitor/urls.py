'''
Monitor/Urls.py - It contains url endpoints for -
1. Dashboard - Retrieve analysis for dashboard (Get)
'''
from django.urls import path
from .views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard')
]

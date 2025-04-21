'''
Cook/Urls.py - It contains url endpoints for -
1. Listing Tasks (Get)
2. Retrieving Tasks (Get and Put)
'''
from django.urls import path
from .views import TaskListView, TaskRetrieveView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>', TaskRetrieveView.as_view(), name='task_retrieve'),
]

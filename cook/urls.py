from django.urls import path
from .views import task_list, get_task

urlpatterns = [
    path('tasks/', task_list.as_view(), name='tasks'),
    path('task/<int:pk>', get_task.as_view(), name='task_retrieve'),
]

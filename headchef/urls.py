from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, MenuListCreateView, MenuRetrieveUpdateDestroyView

urlpatterns = [
    path('task/', TaskListCreateView.as_view(), name="task_list_create"),
    path('task/<int:pk>', TaskRetrieveUpdateDestroyView.as_view(), name="task_retrieve_update_destroy"),
    path('menu/', MenuListCreateView.as_view(), name="menu_list_create"),
    path('menu/<int:pk>', MenuRetrieveUpdateDestroyView.as_view(), name="menu_retrieve_update_destroy")
]

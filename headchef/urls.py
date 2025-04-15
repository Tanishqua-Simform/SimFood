from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, MenuListCreateView, MenuRetrieveUpdateDestroyView, get_will_eat_count, send_jinja_email, render_dtl

urlpatterns = [
    path('task/', TaskListCreateView.as_view(), name="task_list_create"),
    path('task/<int:pk>', TaskRetrieveUpdateDestroyView.as_view(), name="task_retrieve_update_destroy"),
    path('menu/', MenuListCreateView.as_view(), name="menu_list_create"),
    path('menu/<int:pk>', MenuRetrieveUpdateDestroyView.as_view(), name="menu_retrieve_update_destroy"),
    path('count/', get_will_eat_count, name="will_eat"),
    path('mail/', send_jinja_email, name="send_jinja_email"),
    path('dtl/', render_dtl, name="render_dtl")
]

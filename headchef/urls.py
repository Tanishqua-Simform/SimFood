'''
Headchef/Urls.py - It contains url endpoints for -
1. Menu - Listing and Creating (Get and Post)
2. Menu - Retrieving, Updating and Deleting (Get, Put and Delete)
3. Task - Listing and Creating (Get and Post)
4. Task - Retrieving, Updating and Deleting (Get, Put and Delete)
5. Count -  Retrieve count of Employees consuming food today. (Get)
6. Mail - Jinja template for email Menu (Get)
7. DTL - DTL template for Menu (Get)
'''
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

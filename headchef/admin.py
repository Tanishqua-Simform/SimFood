from django.contrib import admin
from .models import TaskModel, MenuModel

admin.site.register(TaskModel)
admin.site.register(MenuModel)
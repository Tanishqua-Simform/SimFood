from rest_framework import serializers
from headchef.models import TaskModel

class TaskCookSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskModel
        fields = ["title", "description", "status", "assigned_by"]
        extra_kwargs = {
            "title" : {
                "read_only": True
            },   
            "description" : {
                "read_only": True
            },
            "assigned_by" : {
                "read_only": True
            }
        }
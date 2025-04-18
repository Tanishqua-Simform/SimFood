from rest_framework import serializers
from headchef.models import TaskModel
from users.models import SimfoodUser

class TaskCookSerializer(serializers.ModelSerializer):
    assigned_by = serializers.SerializerMethodField()

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
    
    def get_assigned_by(self, obj):
        return obj.assigned_by.first_name
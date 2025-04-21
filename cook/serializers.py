'''
Cook/Serializers.py - It contains serializers for -
1. Task - Retrieval of details and updation of status.
'''
from rest_framework import serializers
from headchef.models import TaskModel

class TaskCookSerializer(serializers.ModelSerializer):
    ''' Serializes task data for Cooks to view. '''
    assigned_by = serializers.SerializerMethodField()

    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
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
        ''' To serialize the name of assignee rather than their id.'''
        return obj.assigned_by.first_name
    
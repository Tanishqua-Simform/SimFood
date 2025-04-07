from rest_framework import serializers
from .models import TaskModel, MenuModel
from datetime import datetime
from users.models import SimfoodUser

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskModel
        fields = ["id", "title", "description", "status", "assigned_by", "assigned_to"]
        extra_kwargs = {
            'assigned_by':{
                'read_only': True
                }
            }

    def create(self, validated_data):
        email = self.context['request'].user
        user = SimfoodUser.objects.get(email=email)
        validated_data["assigned_by"] = user
        return TaskModel.objects.create(**validated_data)


class MenuSerializer(serializers.ModelSerializer):
    extras = serializers.MultipleChoiceField(choices=MenuModel.EXTRA_CHOICES)

    class Meta:
        model = MenuModel
        fields = ["id", "date", "dal", "rice", "sabzi", "roti", "extras", "jain_dal", "jain_sabzi", "created_by"]
        extra_kwargs = {
            'created_by':{
                'read_only': True
                }
            }

    def create(self, validated_data):
        email = self.context['request'].user
        user = SimfoodUser.objects.get(email=email)
        validated_data["created_by"] = user
        return MenuModel.objects.create(**validated_data)

    def validate_date(self, date):
        if not datetime.now().date().__lt__(date):
            raise serializers.ValidationError('You can only add menu for future dates!')
        return date
    
    
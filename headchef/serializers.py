from rest_framework import serializers
from .models import TaskModel, MenuModel
from datetime import datetime
from users.models import SimfoodUser

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()
    assigned_by = serializers.SerializerMethodField()

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

    def get_assigned_to(self, obj):
        return obj.assigned_to.first_name
    
    def get_assigned_by(self, obj):
        return obj.assigned_by.first_name

class MenuSerializer(serializers.ModelSerializer):
    extras = serializers.MultipleChoiceField(choices=MenuModel.EXTRA_CHOICES)
    created_by = serializers.SerializerMethodField()

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
    
    def get_created_by(self, obj):
        return obj.created_by.first_name

    def validate_date(self, date):
        if not datetime.now().date().__lt__(date):
            raise serializers.ValidationError('You can only add menu for future dates!')
        return date
    
    def update(self, instance, validated_data):
        ''' So that menu date is modifiable only during creation but not at updation'''
        instance.dal = validated_data.get('dal', instance.dal)
        instance.rice = validated_data.get('rice', instance.rice)
        instance.sabzi = validated_data.get('sabzi', instance.sabzi)
        instance.roti = validated_data.get('roti', instance.roti)
        instance.extras = validated_data.get('extras', instance.extras)
        instance.jain_dal = validated_data.get('jain_dal', instance.jain_dal)
        instance.jain_sabzi = validated_data.get('jain_sabzi', instance.jain_sabzi)
        instance.save()
        return instance
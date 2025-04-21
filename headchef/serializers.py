'''
Headchef/Serializers.py - It contains serializers for -
1. Menu - To view and modify all the relevant fields of Menu Model.
2. Task - To view and modify all the relevant fields of Task Model.
'''
from datetime import datetime
from rest_framework import serializers
from users.models import SimfoodUser
from .models import TaskModel, MenuModel

class TaskSerializer(serializers.ModelSerializer):
    ''' Serializes the Task details for Headchef View'''
    assigned_to_name = serializers.SerializerMethodField()
    assigned_by_name = serializers.SerializerMethodField()

    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
        model = TaskModel
        fields = ["id", "title", "description", "status", "assigned_to", "assigned_to_name", "assigned_by_name"]
        extra_kwargs = {
            'assigned_to': {
                'write_only': True
                }
            }

    def create(self, validated_data):
        ''' Custom create to add headchef details in the Task Object'''
        email = self.context['request'].user
        user = SimfoodUser.objects.get(email=email)
        validated_data["assigned_by"] = user
        return TaskModel.objects.create(**validated_data)

    def get_assigned_to_name(self, obj):
        ''' To show the name of Cook the task is assigned to.'''
        return obj.assigned_to.first_name

    def get_assigned_by_name(self, obj):
        ''' To show the name of Headchef the task is assigned by.'''
        return obj.assigned_by.first_name

    def validate_assigned_to(self, assigned_to):
        ''' To validate that the task is assigned to a user with role of Cook.'''
        if assigned_to.role != 'cook':
            raise serializers.ValidationError('You can only assign task to Cooks.')
        return assigned_to

class MenuSerializer(serializers.ModelSerializer):
    ''' Serializes the Menu details for Headchef View'''
    extras = serializers.MultipleChoiceField(choices=MenuModel.EXTRA_CHOICES)
    created_by = serializers.SerializerMethodField()

    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
        model = MenuModel
        fields = ["id", "date", "dal", "rice", "sabzi", "roti", "extras", "jain_dal", "jain_sabzi", "created_by"]
        extra_kwargs = {
            'created_by':{
                'read_only': True
                }
            }

    def create(self, validated_data):
        ''' Custom create to add headchef details in the Menu Object'''
        email = self.context['request'].user
        user = SimfoodUser.objects.get(email=email)
        validated_data["created_by"] = user
        return MenuModel.objects.create(**validated_data)

    def get_created_by(self, obj):
        ''' To show the name of Headchef who has created the menu.'''
        return obj.created_by.first_name

    def validate_date(self, date):
        ''' To validate the date and allow menu creation and updation for
        only future dates.'''
        if not datetime.now().date() < date:
            raise serializers.ValidationError('You can only add menu for future dates!')
        return date

    def update(self, instance, validated_data):
        ''' So that menu date is modifiable only during creation but not at updation'''
        if instance.date != validated_data.get('date'):
            raise serializers.ValidationError('Cannot change the date of menu!')
        instance.dal = validated_data.get('dal', instance.dal)
        instance.rice = validated_data.get('rice', instance.rice)
        instance.sabzi = validated_data.get('sabzi', instance.sabzi)
        instance.roti = validated_data.get('roti', instance.roti)
        instance.extras = validated_data.get('extras', instance.extras)
        instance.jain_dal = validated_data.get('jain_dal', instance.jain_dal)
        instance.jain_sabzi = validated_data.get('jain_sabzi', instance.jain_sabzi)
        instance.save()
        return instance

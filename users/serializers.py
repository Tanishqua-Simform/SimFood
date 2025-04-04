from rest_framework import serializers
from .models import SimfoodUser
from django.contrib.auth.hashers import make_password
import re

class SimfoodUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimfoodUser
        fields = ['id', 'email', 'first_name', 'last_name', 'prefer_jain_food', 'will_eat', 'password']
        extra_kwargs = {
            'password':{
                'write_only': True
                }
            }

    def validate_email(self, value):
        if not value.endswith('@simformsolutions.com'):
            raise serializers.ValidationError('Please provide valid Company Email for Registration!')
        return value
    
    def validate_password(self, pw):
        return make_password(pw)
'''
Users/Serializers.py - It contains serializers for -
1. SimfoodUserSerializer - To serialize the fields of our Apps Users while registration Process.
'''
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import SimfoodUser

class SimfoodUserSerializer(serializers.ModelSerializer):
    ''' Serializes the relevant information of Simfood User.'''
    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
        model = SimfoodUser
        fields = ['id', 'email', 'first_name', 'last_name', 'prefer_jain_food', 'will_eat', 'password']
        extra_kwargs = {
            'password':{
                'write_only': True
                }
            }

    def validate_email(self, value):
        ''' Validate if emails are of Company's domain or not.'''
        if not value.endswith('@simformsolutions.com'):
            raise serializers.ValidationError('Please provide valid Company Email for Registration!')
        return value

    def validate_password(self, pw):
        ''' Hashes the password in Plain text to ciphered text'''
        return make_password(pw)

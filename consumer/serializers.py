'''
Consumer/Serializers.py - It contains serializers for -
1. Menu - To view all the relevant fields of Menu Model.
2. User Preference - To view will_eat and prefer_jain_food field of User model.
3. Payment Process - To view payment and subscription related fields of User model.
'''
from rest_framework import serializers
from headchef.models import MenuModel
from users.models import SimfoodUser

class MenuViewSerializer(serializers.ModelSerializer):
    ''' Serializes Menu data for Consumers to view.'''

    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
        model = MenuModel
        fields = ["date", "dal", "rice", "sabzi", "roti", "extras", "jain_dal", "jain_sabzi"]
        extra_kwargs = {
            "__all__": {
                "read_only": True
            }
        }

class UserPreferenceSerializer(serializers.ModelSerializer):
    ''' Serializes User Preference data for food related queries.'''

    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
        model = SimfoodUser
        fields = ["will_eat", "prefer_jain_food"]

class PaymentSerializer(serializers.ModelSerializer):
    ''' Serializes Payment data and validates for reverse and/or multiple payments.'''

    class Meta:
        ''' Meta class to define the model and its fields for serializer'''
        model = SimfoodUser
        fields = ["paid_next_month", "subscription_active"]

    def validate_paid_next_month(self, boolean):
        ''' Validate reverse and/or multiple payments.'''
        if not boolean:
            raise serializers.ValidationError('Cannot reverse the payment for next month!')
        if self.context.get("paid_next_month"):
            raise serializers.ValidationError('Cannot make Payment for next month twice!')
        return boolean

    def validate_subscription_active(self, boolean):
        ''' Validate reverse and/or multiple payments.'''
        if not boolean:
            raise serializers.ValidationError('Cannot reverse the payment for current subscription!')
        if self.context.get("subscription_active"):
            raise serializers.ValidationError('Cannot make Payment for Current subscription twice!')
        return boolean

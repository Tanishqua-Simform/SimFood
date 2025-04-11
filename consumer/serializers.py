from rest_framework import serializers
from headchef.models import MenuModel
from users.models import SimfoodUser

class MenuViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuModel
        fields = ["date", "dal", "rice", "sabzi", "roti", "extras", "jain_dal", "jain_sabzi"]
        extra_kwargs = {
            "__all__": {
                "read_only": True
            }
        }

class UserPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimfoodUser
        fields = ["will_eat", "prefer_jain_food"]

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimfoodUser
        fields = ["paid_next_month", "subscription_active"]
    
    def validate_paid_next_month(self, bool):
        if not bool:
            raise serializers.ValidationError('Cannot reverse the payment for next month!')
        if self.context.get("paid_next_month"):
            raise serializers.ValidationError('Cannot make Payment for next month twice!')
        return bool
    
    def validate_subscription_active(self, bool):
        if not bool:
            raise serializers.ValidationError('Cannot reverse the payment for current subscription!')
        if self.context.get("subscription_active"):
            raise serializers.ValidationError('Cannot make Payment for Current subscription twice!')
        return bool
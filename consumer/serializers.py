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
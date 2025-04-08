from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from headchef.models import MenuModel
from users.models import SimfoodUser
from .serializers import MenuViewSerializer, UserPreferenceSerializer
from datetime import datetime, timedelta

class IsSubscribed(BasePermission):
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.subscription_active

class ViewMenuChangeEatPreferenceDaily(APIView):
    permission_classes = [IsAuthenticated & IsSubscribed]
    def get(self, request):
        date = datetime.now().date()
        time = datetime.now().time()
        menu_change_time = datetime.strptime('10:30 AM', '%I:%M %p').time() # 4:00 PM IST in GMT time
        if time >= menu_change_time:
            date += timedelta(days=1)
        menu = MenuModel.objects.filter(date__icontains=date)
        if len(menu) > 0:
            menu_serializer = MenuViewSerializer(menu, many=True)
            user = SimfoodUser.objects.get(email=request.user)
            preference_serializer = UserPreferenceSerializer(user)
            return Response({ 'menu': menu_serializer.data, 'preference': preference_serializer.data} , status=status.HTTP_200_OK)
        data = {
            'status': 'success', 
            'message': 'Menu for tomorrow is not uploaded yet.'
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = SimfoodUser.objects.get(email=request.user)
        preference_serializer = UserPreferenceSerializer(user, data=request.data)
        if preference_serializer.is_valid():
            preference_serializer.save()
            return Response(preference_serializer.data, status=status.HTTP_201_CREATED)
        return Response(preference_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

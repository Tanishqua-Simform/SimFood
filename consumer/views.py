from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from headchef.models import MenuModel
from users.models import SimfoodUser
from .serializers import MenuViewSerializer, UserPreferenceSerializer, PaymentSerializer
from datetime import datetime, timedelta, time

class IsSubscribed(BasePermission):
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.subscription_active

class IsConsumer(BasePermission):
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.role == 'consumer'

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
        # timezone = datetime.tzinfo('IST')
        # request_time = datetime.now().astimezone(timezone).time()
        # disable_from = datetime.strptime('10:00 AM', '%H:%M:%S')
        # disable_till = datetime.strptime('6:00 PM', '%H:%M:%S')
        request_time = datetime.now().time()
        disable_from = time(hour=10, minute=0)
        disable_till = time(hour=18, minute=0)
        if disable_from <= request_time <= disable_till:
            context = {
                'status' : 'failed',
                'error': 'Cannot Change Preference From 10:00 AM to 6:00 PM.'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        user = SimfoodUser.objects.get(email=request.user)
        preference_serializer = UserPreferenceSerializer(user, data=request.data)
        if preference_serializer.is_valid():
            preference_serializer.save()
            return Response(preference_serializer.data, status=status.HTTP_201_CREATED)
        return Response(preference_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated & IsConsumer])
def payment_process(request):
    user = SimfoodUser.objects.get(email=request.user)
    
    if request.method == 'GET':
        serializer = PaymentSerializer(instance=user)
        if user.paid_next_month and user.subscription_active:
            context = {
                'status': 'success',
                'message': 'Your subscription is active and you have paid for next month as well',
            }
        elif user.subscription_active:
            context = {
                'status': 'success',
                'message': 'Your subscription is active. Pay for next month to continue.',
            }
        elif user.paid_next_month:
            context = {
                'status': 'success',
                'message': 'You have paid for next month. Pay for current month to get access for Kitchen.',
            }
        else:
            context = {
                'status': 'success',
                'message': 'You have not subscribed for our delicious meal. Please pay fee for current month or for next month to subscribe.',
            }
        return Response({'Reponse': context, 'User Status': serializer.data}, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        old_data = {
            'paid_next_month': user.paid_next_month,
            'subscription_active': user.subscription_active
        }
        serializer = PaymentSerializer(instance=user, data=request.data, context=old_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'User Status': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
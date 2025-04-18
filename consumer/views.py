from django.shortcuts import render
from django.core.cache import cache
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from headchef.models import MenuModel
from users.models import SimfoodUser
from SimFood.throttle import CustomGetThrottleClass, CustomPutThrottleClass, CustomPaymentPutThrottleClass
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
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]
    def get(self, request):
        # Menu Retrieval
        menu = cache.get('menu')
        if not menu:
            print('Cache Miss MENU')
            date = datetime.now().date()
            time = datetime.now().time()
            menu_change_time = datetime.strptime('6:00 PM', '%I:%M %p').time() # Menu for next day after 6 PM
            if time >= menu_change_time:
                date += timedelta(days=1)
            menu = MenuModel.objects.filter(date__icontains=date)
            cache.set('menu', menu, timeout=60*60*3)
        else:
            print('Cache Hit MENU')
        if len(menu) > 0:
            menu_serializer = MenuViewSerializer(menu, many=True)
            menu_response = menu_serializer.data
        else:
            menu_response = 'Menu for tomorrow is not uploaded yet.'
        
        # user Preference Retrieval
        user = SimfoodUser.objects.get(email=request.user)
        preference_serializer = UserPreferenceSerializer(user)
        data = {
            'message': 'Menu and Preference details retrieval successful',
            'response': { 
                'menu': menu_response, 
                'preference': preference_serializer.data
            }
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request):
        request_time = datetime.now().time()
        disable_from = time(hour=10, minute=0)
        disable_till = time(hour=18, minute=0)
        if disable_from <= request_time <= disable_till:
            data = {
                'message' : 'User Preference updation failed',
                'response': {
                    'error': 'Cannot Change Preference From 10:00 AM to 6:00 PM.'
                }
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        user = SimfoodUser.objects.get(email=request.user)
        preference_serializer = UserPreferenceSerializer(user, data=request.data)
        if preference_serializer.is_valid():
            preference_serializer.save()
            data = {
                'message' : 'User Preference updation successful',
                'response': preference_serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
                'message' : 'User Preference updation failed',
                'response': preference_serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated & IsConsumer])
@throttle_classes([CustomGetThrottleClass, CustomPaymentPutThrottleClass])
def payment_process(request):
    user = SimfoodUser.objects.get(email=request.user)
    
    if request.method == 'GET':
        serializer = PaymentSerializer(instance=user)
        if user.paid_next_month and user.subscription_active:
            payment_status_message = 'Your subscription is active and you have paid for next month as well'

        elif user.subscription_active:
            payment_status_message =  'Your subscription is active. Pay for next month to continue.'

        elif user.paid_next_month:
            payment_status_message = 'You have paid for next month. Pay for current month to get access for Kitchen.'

        else:
            payment_status_message = 'You have not subscribed for our delicious meal. Please pay fee for current month or for next month to subscribe.'

        data = {
                'message': 'Payment status retrieval successful',
                'response': {
                    'payment_status_message': payment_status_message,
                    'payment_status': serializer.data
                }
            }
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        old_data = {
            'paid_next_month': user.paid_next_month,
            'subscription_active': user.subscription_active
        }
        serializer = PaymentSerializer(instance=user, data=request.data, context=old_data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'Payment status updation successful',
                'response': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': 'Payment status updation failed',
            'response': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSubscribed])
def came_to_eat_attendance_scanner(request):
    user = SimfoodUser.objects.get(email=request.user)
    if not user.came_to_eat:
        user.came_to_eat = True
        user.save()
        data = {
            'message': 'Lunch taken status updation successful',
            'response': 'User came_to_eat status set to True'
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {
            'message': 'Lunch taken status updation failed',
            'response': 'Cannot mark attendance twice.'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
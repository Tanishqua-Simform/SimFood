from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from headchef.models import TaskModel
from SimFood.throttle import CustomGetThrottleClass, CustomPutThrottleClass
# from headchef.serializers import TaskSerializer
from users.models import SimfoodUser
from .serializers import TaskCookSerializer
from datetime import datetime

class IsCook(BasePermission):
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.role == 'cook'

class task_list(APIView):
    permission_classes=[IsAuthenticated & IsCook]
    throttle_classes = [CustomGetThrottleClass]
    def get(self, request):
        queryset = TaskModel.objects.filter(assigned_to=request.user, created_at__icontains=datetime.now().date())
        if len(queryset) > 0:
            serializer = TaskCookSerializer(queryset, many=True)
            data = {
                'message': 'Task list retrieval successful',
                'response': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': 'Task list retrieval successful',
            'response': 'For today, No Tasks are created yet.'
        }
        return Response(data, status=status.HTTP_200_OK)


class get_task(APIView):
    permission_classes=[IsAuthenticated & IsCook]
    throttle_scope = ('user-get', 'user-put')
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]
    def get(self, request, pk):
        task = TaskModel.objects.filter(id=pk)
        if len(task) > 0:
            serializer = TaskCookSerializer(task[0])
            data = {
                'message': 'Task details retrieval successful',
                'response': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': 'Task details retrieval failed',
            'response': 'No such Task exists'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = TaskModel.objects.filter(id=pk)
        if len(task) > 0:
            serializer = TaskCookSerializer(task[0], data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'message': 'Task status updation successful',
                    'response': serializer.data
                }
                return Response(data, status=status.HTTP_200_OK)
            data = {
                'message': 'Task status updation failed',
                'response': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'message': 'Task status updation failed',
            'response': 'No such Task exists'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
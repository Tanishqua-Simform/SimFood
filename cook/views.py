'''
Cook/Views.py - It contains views for -
1. Task Listing for that particular cook on that day.
2. Task Detail Retrieval and Updation of status.
'''
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from headchef.models import TaskModel
from users.models import SimfoodUser
from SimFood.throttle import CustomGetThrottleClass, CustomPutThrottleClass
from .serializers import TaskCookSerializer

class IsCook(BasePermission):
    ''' Permits users with role cook to reach specific views.'''
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.role == 'cook'

class TaskListView(APIView):
    ''' Allow Authenticated users with role Cook, to get the list of tasks assigned to
    them on that day.'''
    permission_classes=[IsAuthenticated & IsCook]
    throttle_classes = [CustomGetThrottleClass]
    def get(self, request):
        ''' Retrieves the list of task for User Cook on the day of request.'''
        today = datetime.now().date()
        queryset = TaskModel.objects.filter(assigned_to=request.user, created_at__icontains=today)
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


class TaskRetrieveView(APIView):
    ''' Allow autehnticated users with cook role to retrieve the task by id
    and update only their status.'''
    permission_classes=[IsAuthenticated & IsCook]
    throttle_scope = ('user-get', 'user-put')
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]
    def get(self, request, pk):
        ''' Retrieve the details of the task.'''
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
        ''' Cook can update only the status of the task.'''
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

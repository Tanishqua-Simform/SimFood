from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from headchef.models import TaskModel
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
    def get(self, request):
        queryset = TaskModel.objects.filter(assigned_to=request.user, created_at__icontains=datetime.now().date())
        if len(queryset) > 0:
            serializer = TaskCookSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = {
            'status': 'success',
            'message': 'For today, No Tasks are created yet.'
        }
        return Response(data, status=status.HTTP_200_OK)


class get_task(APIView):
    permission_classes=[IsAuthenticated & IsCook]
    def get(self, request, pk):
        task = TaskModel.objects.get(id=pk)
        serializer = TaskCookSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = TaskModel.objects.get(id=pk)
        serializer = TaskCookSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
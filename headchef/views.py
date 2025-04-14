from django.shortcuts import render
from django.db import connection
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from SimFood.throttle import CustomGetThrottleClass, CustomPutThrottleClass, CustomPostThrottleClass
from users.models import SimfoodUser
from .models import TaskModel, MenuModel
from .serializers import TaskSerializer, MenuSerializer

class IsHeadChef(BasePermission):
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.role == 'headchef'

class TaskListCreateView(generics.ListCreateAPIView):
    queryset=TaskModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=TaskSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPostThrottleClass]

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=TaskModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=TaskSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]

class MenuListCreateView(generics.ListCreateAPIView):
    queryset=MenuModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=MenuSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPostThrottleClass]

class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=MenuSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]

@api_view(['GET'])
@permission_classes([IsAuthenticated & IsHeadChef])
@throttle_classes([CustomGetThrottleClass])
def get_will_eat_count(request):
    eat_jain = SimfoodUser.objects.filter(will_eat=True, prefer_jain_food=True).count()
    eat_regular = SimfoodUser.objects.filter(will_eat=True, prefer_jain_food=False).count()
    content = {
        'going_to_eat_regular': eat_regular,
        'going_to_eat_jain': eat_jain
    }
    return Response(content) 
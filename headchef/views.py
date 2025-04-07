from django.shortcuts import render
from rest_framework import generics
from .models import TaskModel, MenuModel
from .serializers import TaskSerializer, MenuSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset=TaskModel.objects.all()
    serializer_class=TaskSerializer

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=TaskModel.objects.all()
    serializer_class=TaskSerializer

class MenuListCreateView(generics.ListCreateAPIView):
    queryset=MenuModel.objects.all()
    serializer_class=MenuSerializer

class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuModel.objects.all()
    serializer_class=MenuSerializer

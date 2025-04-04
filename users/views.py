from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SimfoodUser
from .serializers import SimfoodUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SimfoodUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(SimfoodUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestingAuth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'status':'success',
            'message':'You are authenticated!'
        }
        return Response(data, status=status.HTTP_200_OK)
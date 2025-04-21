'''
Users/Views.py - It contains views for - 
1. Register to SimFood Application
2. Check Authentication using Protected View.
'''
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import SimfoodUserSerializer

class RegisterView(APIView):
    ''' Allow any user to register to our SimFood App with company's email id.'''
    permission_classes = [AllowAny]

    def post(self, request):
        '''User can register to SimFood using this request.'''
        serializer = SimfoodUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'message': 'User Registration Successful',
                'response': SimfoodUserSerializer(user).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'message': 'User Registration Failed',
            'response': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

class TestingAuth(APIView):
    ''' Protected view to verify if the user is authenticated correctly.'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ''' Response for authenticated people.'''
        data = {
            'message':'You are authenticated!',
            'response': 'Confidential Information.'
        }
        return Response(data, status=status.HTTP_200_OK)

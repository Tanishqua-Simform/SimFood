'''
Headchef/Views.py - It contains views for -
1. Task Listing and Creation.
2. Task retrieval, updation and deletion.
3. Menu Listing and Creation.
4. Menu retrieval, updation and deletion.
5. Retrieve the head count of people going to consume food on that day.
'''
from datetime import date, timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from SimFood.throttle import CustomGetThrottleClass, CustomPutThrottleClass, CustomPostThrottleClass
from users.models import SimfoodUser
from .models import TaskModel, MenuModel
from .serializers import TaskSerializer, MenuSerializer

class IsHeadChef(BasePermission):
    ''' Permit only the users with role Headchef to reach specific views.'''
    def has_permission(self, request, view):
        user = SimfoodUser.objects.get(email=request.user)
        return user.role == 'headchef'

class TaskListCreateView(generics.ListCreateAPIView):
    ''' Task List and Create View for Authenticated users with headchef role.'''
    queryset=TaskModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=TaskSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPostThrottleClass]

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    ''' Task Retrieval, updation and Deletion View for Authenticated users 
    with headchef role.'''
    queryset=TaskModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=TaskSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]

class MenuListCreateView(generics.ListCreateAPIView):
    ''' Menu List and Create View for Authenticated users with headchef role.'''
    queryset=MenuModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=MenuSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPostThrottleClass]

class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    ''' Menu Retrieval, updation and Deletion View for Authenticated users 
    with headchef role.'''
    queryset=MenuModel.objects.all()
    permission_classes=[IsAuthenticated & IsHeadChef]
    serializer_class=MenuSerializer
    throttle_classes = [CustomGetThrottleClass, CustomPutThrottleClass]

@api_view(['GET'])
@permission_classes([IsAuthenticated & IsHeadChef])
@throttle_classes([CustomGetThrottleClass])
def get_will_eat_count(request):
    ''' Allow Authenticated users with headchef role to retrieve the count of 
    people coming to eat.'''
    eat_jain = SimfoodUser.objects.filter(will_eat=True, prefer_jain_food=True).count()
    eat_regular = SimfoodUser.objects.filter(will_eat=True, prefer_jain_food=False).count()
    data = {
        'message': 'Consumers count retrieval successful',
        'response': {
            'going_to_eat_regular': eat_regular,
            'going_to_eat_jain': eat_jain
        }
    }
    return Response(data, status=status.HTTP_200_OK)

def send_jinja_email(request):
    ''' Jinja Email Template for sending Menu.'''
    tomorrow = date.today() + timedelta(days=1)
    user = SimfoodUser.objects.get(email=request.user)
    menu = MenuModel.objects.filter(date=tomorrow).values().first()

    # We made custom filter for this in DTL but using this logic in Jinja instead
    for key in menu:
        val = menu[key]
        if key in ['dal', 'rice', 'sabzi', 'roti', 'jain_sabzi', 'jain_dal']:
            menu[key] = ' '.join([i.capitalize() for i in val.split('_')])
        elif key == 'extras':
            menu[key] = [extras.capitalize() for extras in val]
        elif key == 'date':
            menu[key] = date.strftime(val, '%B %d, %Y')
    context = {
        'username': user.first_name,
        'menu': menu
    }
    text_content = render_to_string('menu.txt', context)
    html_content = render_to_string('menu.html', context)
    mail = EmailMultiAlternatives(
        f'SimFood - Delicious Meal for {menu["date"]}',
        text_content,
        to=['codeblinders5@gmail.com']
        )
    mail.attach_alternative(html_content, 'text/html')
    # mail.send(fail_silently=True)
    mail.send()
    return HttpResponse('Your Mail Has been sent Successfully!')

def render_dtl(request):
    ''' DTL template to show Menu for the day of request.'''
    today = date.today()
    menu = MenuModel.objects.filter(date=today).values().first()
    user = SimfoodUser.objects.get(email=request.user)
    context = {
        'username': user.first_name,
        'menu': menu
    }
    return render(request, 'headchef/menu.html', context)

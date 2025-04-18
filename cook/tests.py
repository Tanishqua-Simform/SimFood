from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import SimfoodUser
from headchef.models import TaskModel

class TaskListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('tasks')
        self.cook = SimfoodUser.objects.create_user(
            email = 'cook@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'cook'
        )
        self.headchef = SimfoodUser.objects.create_user(
            email = 'headchef@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'headchef'
        )

    # Unauthenticated Person
    def test_tasks_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # To receive JWT Token
    def login(self, user_data):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=user_data)
        return response.json()['access']
    
    # Authenticated Person with Headchef Role
    def test_tasks_list_authenticated_not_cook(self):
        headchef = {
            'email': 'headchef@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(headchef)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Authenticated Person with Cook Role
    def test_tasks_list_authenticated_cook(self):
        cook = {
            'email': 'cook@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(cook)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'message': 'Task list retrieval successful',
            'response': 'For today, No Tasks are created yet.'
        }
        self.assertEqual(response.data, data)

class TaskListSerializerTest(APITestCase):
    def setUp(self):
        self.url = reverse('tasks')
        self.cook = SimfoodUser.objects.create_user(
            email = 'cook@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'cook'
        )
        self.headchef = SimfoodUser.objects.create_user(
            email = 'headchef@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'headchef'
        )
        self.task = TaskModel.objects.create(
            title='Prepare Aam Ras',
            description='Make some delicious Aam Ras',
            assigned_by=self.headchef,
            assigned_to=self.cook,
        )
    
    # To receive JWT Token
    def login(self, user_data):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=user_data)
        return response.json()['access']

    def test_task_list_serializer(self):
        cook = {
            'email': 'cook@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(cook)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
                'message': 'Task list retrieval successful',
                'response': [{
                    'title': 'Prepare Aam Ras',
                    'description': 'Make some delicious Aam Ras',
                    'status': 'pending',
                    'assigned_by': self.headchef.first_name
                }]
        }
        self.maxDiff = None
        self.assertEqual(response.data, data)
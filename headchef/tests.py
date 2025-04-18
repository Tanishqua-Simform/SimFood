from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import SimfoodUser 

class GetWillEatCountViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('will_eat')
        self.jain = SimfoodUser.objects.create_user(
            email = 'jain@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            prefer_jain_food = True,
        )
        self.regular = SimfoodUser.objects.create_user(
            email = 'regular@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
        )
        self.headchef = SimfoodUser.objects.create_user(
            email = 'headchef@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            role = 'headchef',
        )

    # To receive JWT Token
    def login(self, user_data):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=user_data)
        return response.json()['access']

    # Unauthenticated Person
    def test_get_will_eat_count_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Authenticated Person with Consumer Role
    def test_get_will_eat_count_authenticated_not_headchef(self):
        jain = {
            'email': 'jain@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(jain)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Authenticated Person with Headchef Role
    def test_get_will_eat_count_authenticated_headchef(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'message': 'Consumers count retrieval successful',
            'response': {
                'going_to_eat_regular': 0,
                'going_to_eat_jain': 0
            }
        }
        self.assertEqual(response.data, data)
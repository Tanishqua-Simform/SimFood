from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import SimfoodUser

class DashboardViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('dashboard')
        self.authenticated = SimfoodUser.objects.create_user(
            email = 'authenticated@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
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
    def test_dashboard_view(self):
        authenticated = {
            'email': 'authenticated@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(authenticated)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
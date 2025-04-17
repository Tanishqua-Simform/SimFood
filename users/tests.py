from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import SimfoodUser

class ProtectedViewTest(APITestCase):
    def setUp(self):
        self.user = SimfoodUser.objects.create_user(
            email = 'test@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
        )
    
    # Login to obtain JWT token
    def login(self):
        url = reverse('token_obtain_pair')
        user_data = {
            'email': 'test@simformsolutions.com',
            'password': 'test@123'
        }
        response = self.client.post(url, data=user_data)
        self.token = response.json()['access']

    # Testing Unauthenticated
    def test_protected_view_unauthenticated(self):
        self.url = reverse('protected')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Testing Authenticated
    def test_protected_view_authenticated(self):
        self.url = reverse('protected')
        self.login()
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        json_content = {
            'message':'You are authenticated!',
            'response': 'Confidential Information.'
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, json_content)
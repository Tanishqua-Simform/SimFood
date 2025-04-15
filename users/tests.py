from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import SimfoodUser

class ProtectedViewTest(APITestCase):
    def setUp(self):
        self.user = SimfoodUser.objects.create_user(
            email = 'tanishqua.bansal8@simformsolutions.com',
            first_name = 'Tanishqua',
            last_name = 'Bansal',
            # role = 'consumer'
            # subscription_active = models.BooleanField(default=False)
            # paid_next_month = models.BooleanField(default=False)
            # prefer_jain_food = models.BooleanField(default=False)
            # will_eat = models.BooleanField(default=False)
            # came_to_eat = models.BooleanField(default=False)
            # is_active = models.BooleanField(default=True)
            # is_staff = models.BooleanField(default=False)
        )
        self.client.force_login(user=self.user)
        self.url = reverse('protected')

    def test_protected_view(self):
        response = self.client.get(self.url)
        json_content = {
            "status": "success",
            "message": "You are authenticated!"
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, json_content)
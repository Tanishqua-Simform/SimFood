from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# from .models import 

class DashboardViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('dashboard')

    def test_dashboard_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # data = {
        #     'message': 'Data Retrieval Successful',
        #     'response': {
        #         'served-people-last-7-days': 'No data available.',
        #         'prev-month-food-analysis-in-kgs': 'Previous month data not available.'
        #     }
        # }
        # self.assertEqual(response.data, data)
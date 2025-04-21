from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import SimfoodUser
from headchef.models import MenuModel
from .serializers import UserPreferenceSerializer, MenuViewSerializer

class MenuViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('view_menu_change_preference')
        self.subscribed_user = SimfoodUser.objects.create_user(
            email = 'subscribed@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True
        )
        self.not_subscribed_user = SimfoodUser.objects.create_user(
            email = 'unsubscribed@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = False
        )
        self.headchef = SimfoodUser.objects.create_user(
            email = 'headchef@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'headchef'
        )
        self.today_menu = MenuModel.objects.create(
            date = "2025-04-21",
            dal = "gujarati_dal",
            rice = "jeera_rice",
            sabzi = "aloo_bhindi",
            roti = "plain_roti",
            extras = [
                "patra",
                "jaggery",
                "pickle",
                "pappad",
                "salad"
            ],
            jain_dal = "mix_dal",
            jain_sabzi = "kela_nu_shak",
            created_by = self.headchef
        )
        self.tomorrow_menu = MenuModel.objects.create(
            date = "2025-04-22",
            dal = "mix_dal",
            rice = "plain_rice",
            sabzi = "butter_paneer",
            roti = "parantha",
            extras = [
                "dhokla",
                "jaggery",
                "pickle",
                "pappad",
                "salad"
            ],
            jain_dal = "mix_dal",
            jain_sabzi = "pappad_nu_shak",
            created_by = self.headchef
        )

    # To receive JWT Token
    def login(self, user_data):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=user_data)
        return response.json()['access']
    
    # Unauthenticated Person
    def test_menu_and_preference_view_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Authenticated Person with Inactive subscription
    def test_menu_and_preference_view_authenticated_not_subscribed(self):
        not_subscribed_user = {
            'email': 'unsubscribed@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(not_subscribed_user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Authenticated Person with Active subscription
    def test_menu_and_preference_view_authenticated_subscribed(self):
        subscribed_user = {
            'email': 'subscribed@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(subscribed_user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menu_and_preference_view_response(self):
        subscribed_user = {
            'email': 'subscribed@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(subscribed_user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        menu_serializer = MenuViewSerializer(instance=self.tomorrow_menu)
        preference_serializer = UserPreferenceSerializer(instance=self.subscribed_user)
        data = {
            'message': 'Menu and Preference details retrieval successful',
            'response': { 
                'menu': [menu_serializer.data], 
                'preference': preference_serializer.data
            }
        }
        self.assertEqual(response.data, data)

class PaymentProcessViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('payment_process')
        self.headchef = SimfoodUser.objects.create_user(
            email = 'headchef@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'headchef'
        )
        self.cook = SimfoodUser.objects.create_user(
            email = 'cook@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'cook'
        )
        self.consumer_both_inactive = SimfoodUser.objects.create_user(
            email = 'consumer_both_inactive@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            role = 'consumer'
        )
        self.consumer_both_active = SimfoodUser.objects.create_user(
            email = 'consumer_both_active@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            paid_next_month = True,
            role = 'consumer'
        )
        self.consumer_next_active = SimfoodUser.objects.create_user(
            email = 'consumer_next_active@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            paid_next_month = True,
            role = 'consumer'
        )
        self.consumer_curr_active = SimfoodUser.objects.create_user(
            email = 'consumer_curr_active@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'consumer'
        )
    
    # To receive JWT Token
    def login(self, user_data):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=user_data)
        return response.json()['access']

    # Unauthenticated Person
    def test_payment_view_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Authenticated Person with Headchef Role
    def test_payment_view_authenticated_headchef(self):
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
    def test_payment_view_authenticated_cook(self):
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Authenticated Person with Consumer Role
    def test_payment_view_authenticated_consumer(self):
        consumer_curr_active = {
            'email': 'consumer_curr_active@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(consumer_curr_active)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Authenticated Person with Consumer Role Paying Current and Next
    def test_payment_view_authenticated_consumer_pay_both(self):
        consumer_both_inactive = {
            'email': 'consumer_both_inactive@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(consumer_both_inactive)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        data = {
            "paid_next_month": True,
            "subscription_active": True
        }   
        response = self.client.put(self.url, headers=headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Authenticated Person with Consumer Role Reverse Payment
    def test_payment_view_authenticated_consumer_reverse_payment(self):
        consumer_both_active = {
            'email': 'consumer_both_active@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(consumer_both_active)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        data = {
            "paid_next_month": False,
            "subscription_active": False
        }   
        response = self.client.put(self.url, headers=headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CameToEatScannerViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('scanner')
        self.active_consumer = SimfoodUser.objects.create_user(
            email = 'active_consumer@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'headchef'
        )
        self.inactive_consumer = SimfoodUser.objects.create_user(
            email = 'inactive_consumer@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
        )
        self.headchef = SimfoodUser.objects.create_user(
            email = 'headchef@simformsolutions.com', 
            password = 'test@123',
            first_name = 'Test',
            last_name = 'Case',
            subscription_active = True,
            role = 'headchef'
        )

    # To receive JWT Token
    def login(self, user_data):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=user_data)
        return response.json()['access']

    # Unauthenticated Person
    def test_scanner_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Authenticated Person with Inactive Subscription
    def test_scanner_authenticated_inactive_consumer(self):
        inactive_consumer = {
            'email': 'inactive_consumer@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(inactive_consumer)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Authenticated Person with Active Subscription
    def test_scanner_authenticated_active_consumer(self):
        active_consumer = {
            'email': 'active_consumer@simformsolutions.com',
            'password': 'test@123'
        }
        token = self.login(active_consumer)
        headers = {
            'Authorization': f'Bearer {token}',
            'Cookie': 'csrftoken=k9Uhq7wciYP5iWaF8qa1zPBb99f6ideP'
        }
        # Mark Attendace once
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Mark Attendance Twice gives error
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Authenticated Person with Headchef Role
    def test_scanner_authenticated_headchef(self):
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
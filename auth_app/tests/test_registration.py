from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status



class registrationTest(APITestCase):

    def setUp(self):
        self.url = reverse("registration")
        self.valid_data_customer = {
            "username": "customerUser",
            "email": "customer@mail.de",
            "password": "securePassword123",
            "repeated_password": "securePassword123",
            "type": "customer"
        }
        self.valid_data_business = {
            "username": "businessUser",
            "email": "business@mail.de",
            "password": "securePassword123",
            "repeated_password": "securePassword123",
            "type": "business"
        }

    def test_registration_customer_success(self):
        response = self.client.post(self.url, self.valid_data_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_registration_business_success(self):
        response = self.client.post(self.url, self.valid_data_business, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
    
    def test_registration_password_mismatch(self):
        data = self.valid_data_customer.copy()
        data["repeated_password"] = "wrongPassword"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_registration_email_duplicate(self):
        self.client.post(self.url, self.valid_data_customer, format="json")
        data = self.valid_data_customer.copy()
        data["username"] = "otherUser"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_invalid_user_type(self):
        data = self.valid_data_customer.copy()
        data["type"] = "invalid_type"
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("type", response.data)
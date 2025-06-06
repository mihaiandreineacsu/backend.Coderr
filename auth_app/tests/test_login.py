from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..models import UserProfile
from ..api.serializers import RegistrationsSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BaseUserSetup(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword2",
        )
        UserProfile.objects.create(user=cls.user, type="customer")


#TODO: Login tests !
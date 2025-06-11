from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from auth_app.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles_app.models import Profile


class ProfileTestSetup(APITestCase):

    def setUp(self):
        # Test Users erstellen
        self.business_user = User.objects.create_user(
            username="business_test",
            email="business@test.com",
            password="testpass123",
            first_name="Max",
            last_name="Muster",
        )

        self.customer_user = User.objects.create_user(
            username="customer_test",
            email="customer@test.com",
            password="testpass123",
            first_name="Jane",
            last_name="Sonomo",
        )

        # UserProfiles erstellen
        self.business_profile = UserProfile.objects.create(
            user=self.business_user, type="business"
        )

        self.customer_profile = UserProfile.objects.create(
            user=self.customer_user, type="customer"
        )

        # Tokens für Authentication erstellen
        self.business_token = Token.objects.create(user=self.business_user)
        self.customer_token = Token.objects.create(user=self.customer_user)

        # APIClient setup
        self.client = APIClient()

    def authenticate_user(self, user_type="business"):
        """Helper method um User zu authentifizieren."""
        if user_type == "business":
            self.client.credentials(
                HTTP_AUTHORIZATION="Token " + self.business_token.key
            )
        elif user_type == "customer":
            self.client.credentials(
                HTTP_AUTHORIZATION="Token " + self.customer_token.key
            )

    def clear_authentication(self):
        """Helper method um Authentication zu entfernen."""
        self.client.credentials()


class profileTest(ProfileTestSetup):

    def setUp(self):
        super().setUp()
        self.profile_json = {
            "user": 1,
            "username": "",
            "first_name": "",
            "last_name": "",
            "file": "profile_picture.jpg",
            "location": "",
            "tel": "",
            "description": "",
            "working_hours": "",
            "type": "",
            "email": "",
            "created_at": "",
        }
        self.types = ["business", "customer"]

    def test_get_profile_authenticated(self):

        for i in self.types:
            self.authenticate_user(i)

            if i == "business":
                profile = self.business_profile.profile
            elif i == "customer":
                profile = self.customer_profile.profile

            url = reverse("profile-detail", kwargs={"pk": profile.id})
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            expected_keys = set(self.profile_json.keys())
            response_keys = set(response.data.keys())

            self.assertEqual(expected_keys, response_keys)

            self.assertEqual(response.data["first_name"], profile.first_name)
            self.assertEqual(response.data["location"], "")
            self.assertEqual(response.data["type"], i)
            self.clear_authentication()

    def test_get_profile_unauthenticated(self):
        profile_id = self.business_profile.profile.id
        url = reverse("profile-detail", kwargs={"pk": profile_id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_nonexistent_profile(self):
        self.authenticate_user("business")
        url = reverse("profile-detail", kwargs={"pk": 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_own_profile_success(self):
        self.authenticate_user("business")

        profile_id = self.business_profile.profile.id
        url = reverse("profile-detail", kwargs={"pk": profile_id})

        update_data = {
            "first_name": "Updated Max",
            "location": "München",
            "description": "Updated Business Description",
        }

        response = self.client.patch(url, update_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_keys = set(self.profile_json.keys())
        response_keys = set(response.data.keys())
        self.assertEqual(expected_keys, response_keys)

        self.assertEqual(response.data["first_name"], update_data["first_name"])
        self.assertEqual(response.data["location"], update_data["location"])

        # Verify database was updated
        self.business_user.refresh_from_db()
        self.assertEqual(self.business_user.first_name, update_data["first_name"])

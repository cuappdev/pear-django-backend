import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class PearTestCase(TestCase):
    AUTHENTICATE_URL = reverse("authenticate")
    FIRST_NAME = "Gonzalo"
    LAST_NAME = "Gonzalez"
    EMAIL = "gg387@cornell.edu"

    def setUp(self):
        self.client = APIClient()

    def _create_user_and_login(
        self,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        email=EMAIL,
    ):
        """Returns the auth token."""
        data = {
            "sub": "googleID",
            "given_name": first_name,
            "family_name": last_name,
            "email": email,
            "has_onboarded": True,
        }
        response = self.client.post(self.AUTHENTICATE_URL, data)
        self.assertEqual(response.status_code, 201)

        token = json.loads(response.content)["data"]["access_token"]
        return token

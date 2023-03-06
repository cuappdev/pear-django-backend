import json

from api.tests import PearTestCase
from django.urls import reverse
from rest_framework.test import APIClient


class UserProfileTests(PearTestCase):
    ME_URL = reverse("me")
    USERS_URL = reverse("users")

    def setUp(self):
        self.client = APIClient()
        self.user_token = self._create_user_and_login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token)

    def test_get_me(self):

        response = self.client.get(self.ME_URL, format="json")

        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 200)
        data = content.get("data")
        self.assertIn("id", data)
        self.assertIn("net_id", data)
        self.assertIn("first_name", data)
        self.assertIn("last_name", data)

    def test_get_users(self):
        response = self.client.get(self.USERS_URL, format="json")
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        response = self.client.get(self.ME_URL, format="json")
        request_data = {"family_name": "Pumariega"}
        response = self.client.post(self.ME_URL, request_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Gonzalez")

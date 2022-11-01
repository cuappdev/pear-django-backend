from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
import json
from prompt.models import Prompt
from api.tests import PearTestCase
from django.urls import reverse
from rest_framework.test import APIClient


class PromptTestCase(APITestCase):

    def setUp(self):
        pear_test_case = PearTestCase()
        pear_test_case.setUp()
        self.user_token = pear_test_case._create_user_and_login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_token)

    def populate(self):
        """populates the database"""
        url = reverse("populate")
        return self.client.post(url, {"filenames": ["pear_prompts.txt"]}, format='json')

    def test_populate_prompts(self):
        """tests that the code populates the 27 prompts in pear_prompts.txt"""

        response = self.populate()
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Prompt.objects.count(), 27)

    def test_repopulate(self):
        """test repopulate"""

    def test_get_all_prompts(self):
        """tests getting all the promts"""
        populate = self.populate()

        url = reverse("prompts")
        response = self.client.get(url, format='json')
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 200)

    def test_get_prompt_by_id(self):
        """tests getting a promt by a valid id"""
        poulate = self.populate()

        url = reverse("prompt", args=[1])
        response = self.client.get(url, format='json')
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 200)
        data = content.get("data")
        self.assertIn("id", data)
        self.assertIn("question_name", data)
        self.assertIn("question_placeholder", data)

    def test_get_invalid_prompt(self):
        """tests getting an invalid prompt"""
        poulate = self.populate()

        url = reverse("prompt", args=[1000])
        response = self.client.get(url, format='json')
        content = json.loads(response.content)
        self.assertFalse(content.get("sucess"))
        self.assertEqual(response.status_code, 404)

    def test_create_prompt(self):
        """tests creating a valid prompt"""
        poulate = self.populate()
        url = reverse("prompts")

        data = {"question_name": "My favorite animal is ...",
                "question_placeholder": "I really like the animal ..."}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 201)
        data = content.get("data")
        self.assertIn("id", data)
        self.assertIn("question_name", data)
        self.assertIn("question_placeholder", data)

    def test_create_invalid_prompt(self):
        """tests creating an invalid prompt"""
        poulate = self.populate()

        url = reverse("prompts")
        data = {"question": "some question"}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertFalse(content.get("success"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", content)

    def test_create_existing_prompt(self):
        """tests creating already existing prompt"""
        poulate = self.populate()
        url = reverse("prompts")

        data = {"question_name": "Why are you on Pear?",
                "question_placeholder": "I'm on Pear because..."}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        data = content.get("data")
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", data)
        self.assertIn("question_name", data)
        self.assertIn("question_placeholder", data)

    def test_update_prompt(self):
        """tests updating a valid prompt """
        poulate = self.populate()
        url = reverse("prompt", args=[1])

        data = {"question_name": "Why are you on Pear?",
                "question_placeholder": "I am on Pear ..... "}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 200)
        data = content.get("data")
        self.assertIn("id", data)
        self.assertIn("question_name", data)
        self.assertIn("question_placeholder", data)

    def test_update_invalid_prompt(self):
        """tests updating invalid prompt"""
        poulate = self.populate()
        url = reverse("prompt", args=[100])

        data = {"question_name": "anything",
                "question_placeholder": "anything"}
        response = self.client.post(url, data, format='json')
        content = json.loads(response.content)
        self.assertFalse(content.get("success"))
        self.assertEqual(response.status_code, 404)

    def test_delete_prompt(self):
        """tests deleting a valid prompt"""
        poulate = self.populate()
        url = reverse("prompt", args=[1])

        response = self.client.delete(url, format='json')
        content = json.loads(response.content)
        self.assertTrue(content.get("success"))
        self.assertEqual(response.status_code, 200)
        data = content.get("data")
        self.assertIn("id", data)
        self.assertIn("question_name", data)
        self.assertIn("question_placeholder", data)

    def test_delete_invalid_prompt(self):
        """tests deleting an invalid prompt"""
        poulate = self.populate()
        url = reverse("prompt", args=[100])

        response = self.client.delete(url, format='json')
        content = json.loads(response.content)
        self.assertFalse(content.get("success"))
        self.assertEqual(response.status_code, 404)

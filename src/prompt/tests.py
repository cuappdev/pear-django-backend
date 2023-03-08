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
        self.populate()

    def populate(self):
        """Populates the database"""

        url = reverse("populate")

        return self.client.post(url, {"filenames": ["pear_prompts.txt"]}, format='json')

    def assert_helper(self, response, status_code, success, fields):
        """Asserts contents of response are accurate"""

        content = json.loads(response.content)

        if success:
            self.assertTrue(content.get("success"))
        else:
            self.assertFalse(content.get("success"))
        self.assertEqual(response.status_code, status_code)
        if fields:
            data = content.get("data")
            self.assertIn("id", data)
            self.assertIn("question_name", data)
            self.assertIn("question_placeholder", data)

    def prompt_response(self, arg, type, data=None):
        """Generates the response for any tests on a specific prompt"""

        url = reverse("prompt", args=[arg])

        if type == "get":
            return self.client.get(url, format='json')
        elif type == "post":
            return self.client.post(url, data, format='json')
        else:
            return self.client.delete(url, format='json')

    def prompts_response(self, type, data=None):
        """Generates the response for any tests on many prompts"""

        url = reverse("prompts")

        if type == "get":
            return self.client.get(url, format='json')
        else:
            return self.client.post(url, data, format='json')

    def test_repopulate_prompts(self):
        """Tests that the code repopulates prompts in pear_prompts.txt"""

        response = self.populate()

        self.assert_helper(response, 200, True, False)
        self.assertTrue(Prompt.objects.count() > 0)

    def test_get_all_prompts(self):
        """Tests getting all the prompts"""

        self.assert_helper(self.prompts_response("get"), 200, True, False)

    def test_get_prompt_by_id(self):
        """Tests getting a prompt by a valid id"""

        self.assert_helper(self.prompt_response(1, "get"), 200, True, True)

    def test_get_invalid_prompt(self):
        """Tests getting an invalid prompt"""

        self.assert_helper(self.prompt_response(1000, "get"), 404, False, False)

    def test_create_prompt(self):
        """Tests creating a valid prompt"""

        data = {"question_name": "My favorite animal is ...",
                "question_placeholder": "I really like the animal ..."}

        self.assert_helper(self.prompts_response("post", data), 201, True, True)

    def test_create_invalid_prompt(self):
        """Tests creating an invalid prompt"""

        data = {"question": "some question"}

        self.assert_helper(self.prompts_response("post", data), 400, False, False)

    def test_create_existing_prompt(self):
        """Tests creating already existing prompt"""

        data = {"question_name": "Why are you on Pear?",
                "question_placeholder": "I'm on Pear because..."}

        self.assert_helper(self.prompts_response("post", data), 200, True, True)

    def test_update_prompt(self):
        """Tests updating a valid prompt"""

        data = {"question_name": "Why are you on Pear?",
                "question_placeholder": "I am on Pear ..... "}

        self.assert_helper(self.prompt_response(1, "post", data), 200, True, True)

    def test_update_invalid_prompt(self):
        """Tests updating invalid prompt"""

        data = {"question_name": "anything",
                "question_placeholder": "anything"}

        self.assert_helper(self.prompt_response(100, "post", data), 404, False, False)

    def test_delete_prompt(self):
        """Tests deleting a valid prompt"""

        self.assert_helper(self.prompt_response(1, "delete"), 200, True, True)

    def test_delete_invalid_prompt(self):
        """Tests deleting an invalid prompt"""

        self.assert_helper(self.prompt_response(100, "delete"), 404, False, False)

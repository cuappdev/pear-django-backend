import os
from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core import signing
from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from person.models import Person
from rest_framework.authtoken.models import Token


class AuthenticateController:
    PASSWORD_SALT = api_settings.AUTH_PASSWORD_SALT
    TOKEN_AGE = api_settings.ACCESS_TOKEN_AGE

    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer
        self._id_token = data.get("id_token")

    def _issue_access_token(self, user, salt):
        if not user:
            return failure_response("Can only issue token to existing users.")
        if salt == "login":
            token, _ = Token.objects.get_or_create(user=user)
        else:
            token = signing.dumps({"id": user.id}, salt=salt)
        return token.key

    def _get_user_from_token(self, token, salt):
        try:
            value = signing.loads(token, salt=self.PASSWORD_SALT, max_age=900)
        except signing.SignatureExpired:
            return None
        except signing.BadSignature:
            return None
        user_exists = User.objects.filter(id=value.get("id"))
        if user_exists:
            return User.objects.get(id=value.get("id"))
        return None

    def _create_user(self, user_data):
        return User.objects._create_user(**user_data)

    def _create_person(self, person_data):
        person = Person(**person_data)
        person.save()
        return person

    def _check_token(self, token):
        # Allow dummy authentication if debugging
        if not os.getenv('DEBUG', False):
            try:
                idinfo = id_token.verify_oauth2_token(token, requests.Request())
                userid = idinfo['sub']
            except ValueError:
                return False
        return True

    def process(self):
        response = self.login()
        if not response:
            return self.register()
        return response

    def login(self):
        person_exists = Person.objects.filter(id_token=self._id_token)
        if not person_exists:
            return None
        person = Person.objects.get(id_token=self._id_token)
        if not self._check_token(self._id_token):
            return failure_response("ID Token is not valid.")
        login(self._request, person.user)
        access_token = self._issue_access_token(person.user, "login")
        return success_response(
            self._serializer(person.user, context={"access_token": access_token}).data
        )

    def register(self):
        if not self._check_token(self._id_token):
            return failure_response("ID Token is not valid.")
        user_data = {
            "username": "testusername" + str(timezone.now()),
            "password": "testpassword",
            "email": "",
        }
        user = self._create_user(user_data)
        person_data = {
            "user": user,
            "id_token": self._id_token,
        }
        self._create_person(person_data)
        login(self._request, user)
        access_token = self._issue_access_token(user, "login")
        return success_response(
            self._serializer(user, context={"access_token": access_token}).data
        )

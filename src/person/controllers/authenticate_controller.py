import os

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils import timezone
from google.auth.transport import requests
from google.oauth2 import id_token
from person.models import Person
from rest_framework import status
from rest_framework.authtoken.models import Token


class AuthenticateController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def _issue_access_token(self, user):
        """Returns a new access token for `user` if expired; otherwise, returns the original access token."""
        token, _ = Token.objects.get_or_create(user=user)
        elapsed_seconds = (timezone.now() - token.created).total_seconds()
        if api_settings.ACCESS_TOKEN_AGE <= elapsed_seconds:
            token.delete()
            token = Token.objects.create(user=user)
        return token.key

    def _create_user(self, user_data):
        """Returns a newly created User object from `user_data`."""
        return User.objects.create_user(**user_data)

    def _create_person(self, person_data):
        """Returns a newly created Person object from `person_data`."""
        person = Person(**person_data)
        person.save()
        return person

    def _get_token_info(self, token):
        """Returns token information if `token` is valid. If in `DEBUG` mode, returns the request data."""
        if not os.getenv("DEBUG", False):
            try:
                return id_token.verify_oauth2_token(token, requests.Request())
            except ValueError:
                return None
        return self._data

    def _prepare_token_info(self, token_info):
        """Returns relevant information from `token_info`."""
        username = token_info.get("email")
        google_user_id = token_info.get("sub")
        password = api_settings.AUTH_PASSWORD_SALT + google_user_id
        first_name = token_info.get("given_name")
        last_name = token_info.get("family_name")
        profile_pic_url = token_info.get("picture")
        net_id = token_info.get("email").split("@")[0]
        return net_id, username, password, first_name, last_name, profile_pic_url

    def process(self):
        """Returns the current access token or a new one if expired. If the user isn't authenticated yet,
        logs an existing user in or registers a new one."""
        current_user = self._request.user
        status_code = status.HTTP_200_OK
        if not current_user.is_authenticated:
            token = self._data.get("id_token")
            token_info = self._get_token_info(token)
            if token_info is None:
                return failure_response("ID Token is not valid.")
            current_user, status_code = self.login(token_info)
            if current_user is None:
                return failure_response("ID Token is not valid.", status=status_code)
        access_token = self._issue_access_token(current_user)
        return success_response(
            self._serializer(current_user, context={"access_token": access_token}).data,
            status=status_code,
        )

    def login(self, token_info):
        """Returns the authenticated user (if no issues) and status code depending on
        whether a new user registered."""
        net_id, username, password, _, _, _ = self._prepare_token_info(token_info)
        person_exists = Person.objects.filter(net_id=net_id)
        if not person_exists:
            self.register(token_info)
        authenticated_user = authenticate(
            self._request, username=username, password=password
        )
        if authenticated_user is None:
            # Google User ID doesn't correspond to net_id
            # Could result from debugging mistake or malicious activity...
            return None, status.HTTP_403_FORBIDDEN
        login(self._request, authenticated_user)
        return (
            authenticated_user,
            status.HTTP_201_CREATED if not person_exists else status.HTTP_200_OK,
        )

    def register(self, token_info):
        """Creates and associates a User and Person object."""
        (
            net_id,
            username,
            password,
            first_name,
            last_name,
            profile_pic_url,
        ) = self._prepare_token_info(token_info)
        user_data = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
        }
        user = self._create_user(user_data)
        person_data = {
            "user": user,
            "net_id": net_id,
            "profile_pic_url": profile_pic_url,
        }
        self._create_person(person_data)

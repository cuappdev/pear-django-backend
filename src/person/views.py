import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status

from .controllers.authenticate_controller import AuthenticateController
from .controllers.search_person_controller import SearchPersonController
from .controllers.update_person_controller import UpdatePersonController
from .serializers import AllMatchesSerializer
from .serializers import AuthenticateSerializer
from .serializers import SimpleUserSerializer
from .serializers import UserSerializer


class AuthenticateView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer
    permission_classes = api_settings.UNPROTECTED

    def post(self, request):
        """Authenticate the current user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return AuthenticateController(request, data, self.serializer_class).process()


class MeView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get current authenticated user."""
        return success_response(
            self.serializer_class(request.user).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Update current authenticated user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdatePersonController(
            request.user, data, self.serializer_class
        ).process()


class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get user by id."""
        user = User.objects.filter(id=id)
        if not user:
            return failure_response("User not found.", status.HTTP_404_NOT_FOUND)
        return success_response(self.serializer_class(user[0]).data, status.HTTP_200_OK)


class UsersView(generics.GenericAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get users requested with search query."""
        return SearchPersonController(request.GET, self.serializer_class).process()


class AllMatchesView(generics.GenericAPIView):
    serializer_class = AllMatchesSerializer

    def get(self, request, id):
        """Get all matches for user by user id."""
        user = User.objects.filter(id=id)
        if not user:
            return failure_response("User not found.", status.HTTP_404_NOT_FOUND)
        return success_response(self.serializer_class(user[0]).data, status.HTTP_200_OK)

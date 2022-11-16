import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from person.controllers.mass_message_controller import MassMessageController
from rest_framework import generics
from rest_framework import status

from .controllers.authenticate_controller import AuthenticateController
from .controllers.ping_person_controller import PingPersonController
from .controllers.search_person_controller import SearchPersonController
from .controllers.send_message_controller import SendMessageController
from .controllers.update_person_controller import UpdatePersonController
from .serializers import AuthenticateSerializer
from .serializers import UserSerializer
from .simple_serializers import SimpleUserSerializer


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

    def delete(self, request):
        """Soft-delete current authenticated user."""
        data = {"deleted": True}
        return UpdatePersonController(
            request.user, data, self.serializer_class
        ).process()


class PingView(generics.GenericAPIView):
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
        return PingPersonController(request.user, data, self.serializer_class).process()


class UserView(generics.GenericAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get user by id."""
        if not User.objects.filter(id=id).exists():
            return failure_response("User not found.", status.HTTP_404_NOT_FOUND)
        serialized_user = self.serializer_class(
            User.objects.get(id=id), context={"request_user": request.user}
        )
        # because we pass in the request, must make sure serializer is valid
        return success_response(serialized_user.data, status.HTTP_200_OK)


class UsersView(generics.GenericAPIView):
    serializer_class = SimpleUserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get users requested with search query."""
        return SearchPersonController(request, self.serializer_class).process()


class SendMessageView(generics.GenericAPIView):
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request, id):
        """Send message push notification to user by user id."""
        return SendMessageController(request.user, request.data, id).process()


class MassMessageView(generics.GenericAPIView):
    permission_classes = api_settings.ADMIN_PERMISSIONS

    def post(self, request):
        """Send custom push notification to multiple users by id."""
        return MassMessageController(request.data).process()


class BlockUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request, id):
        """Block user by id."""
        if not User.objects.filter(id=id).exists():
            return failure_response("User not found.", status.HTTP_404_NOT_FOUND)
        if request.user.person.blocked_users.filter(id=id).exists():
            # User is already blocked
            return success_response(status=status.HTTP_200_OK)
        elif request.user.id == id:
            return failure_response(
                "You cannot block yourself.", status.HTTP_403_FORBIDDEN
            )
        else:
            request.user.person.blocked_users.add(id)
            return success_response(status=status.HTTP_201_CREATED)


class UnblockUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request, id):
        """Unblock user by id."""
        if not User.objects.filter(id=id).exists():
            return failure_response("User not found.", status.HTTP_404_NOT_FOUND)
        elif id == request.user.id:
            return failure_response(
                "You cannot unblock yourself.", status.HTTP_403_FORBIDDEN
            )
        elif request.user.person.blocked_users.filter(id=id).exists():
            request.user.person.blocked_users.remove(id)
            return success_response(status=status.HTTP_201_CREATED)
        else:
            # User is not blocked anyways
            return success_response(status=status.HTTP_200_OK)

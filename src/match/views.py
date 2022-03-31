import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from django.db.models import Q
from match import match_status
from match.models import Match
from match.serializers import BothUsersMatchSerializer
from match.serializers import MatchSerializer
from pear_algorithm.src.main import main as pear_algorithm
from rest_framework import generics
from rest_framework import status

from .controllers.create_match_controller import CreateMatchController
from .controllers.update_match_controller import UpdateMatchController


class MyMatchesView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all of a user's matches, excluding blocked users."""
        user = request.user
        blocked_ids = user.person.blocked_users.values_list("id", flat=True)
        matches = (
            Match.objects.filter(Q(user_1=user) | Q(user_2=user))
            .exclude(Q(user_1_id__in=blocked_ids) | Q(user_2_id__in=blocked_ids))
            .order_by("-created_date")
        )
        return success_response(self.serializer_class(matches, many=True).data)

    def post(self, request):
        """Create a match."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateMatchController(data, self.serializer_class).process()


class UserMatchesView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer

    def get(self, request, id):
        """Get all matches for user by user id."""
        user = User.objects.filter(id=id).exists()
        if not user:
            return failure_response("User not found.", status.HTTP_404_NOT_FOUND)
        user = User.objects.get(id=id)
        matches = Match.objects.filter(Q(user_1=user) | Q(user_2=user)).order_by(
            "-created_date"
        )
        return success_response(
            self.serializer_class(matches, many=True).data, status.HTTP_200_OK
        )


class AllMatchesView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.ADMIN_PERMISSIONS

    def get(self, request):
        """Get all matches."""
        matches = Match.objects.all().order_by("-created_date")
        return success_response(self.serializer_class(matches, many=True).data)


class MultipleMatchesView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.ADMIN_PERMISSIONS

    def post(self, request):
        """Create multiple matches."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        match_ids_list = data.get("matches")
        cancel_previous = data.get("cancel_previous", False)
        if not match_ids_list:
            return failure_response(
                "POST body is misformatted", status=status.HTTP_400_BAD_REQUEST
            )
        errors = []
        for match_ids in match_ids_list:
            new_match_response = CreateMatchController(
                {"ids": match_ids, "cancel_previous": cancel_previous},
                self.serializer_class,
            ).process()
            if new_match_response.status_code not in [
                status.HTTP_201_CREATED,
                status.HTTP_200_OK,
            ]:
                errors.append(new_match_response)
        if errors:
            return failure_response(
                f"message: {len(errors)} matches failed to be created with the following errors: {errors}",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return success_response(status=status.HTTP_201_CREATED)


class MatchView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get match by id."""
        match = Match.objects.filter(id=id)
        if match:
            return success_response(
                self.serializer_class(match[0]).data, status.HTTP_200_OK
            )
        return failure_response("Match does not exist", status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        """Update match by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateMatchController(
            id, request.user, data, self.serializer_class
        ).process()

    def delete(self, request, id):
        """Delete a match by id."""
        match = Match.objects.filter(id=id)
        if not match:
            return failure_response("Match does not exist", status.HTTP_404_NOT_FOUND)
        match[0].delete()
        return success_response()


class CancelMatchView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request, id):
        """Cancel match by id."""
        match = Match.objects.filter(id=id)
        if not match:
            return failure_response("Match does not exist.", status.HTTP_404_NOT_FOUND)
        match[0].status = match_status.CANCELED
        match[0].save()
        return success_response()


class CurrentMatchView(generics.GenericAPIView):
    serializer_class = MatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get current match by user."""
        match = Match.objects.filter(
            Q(user_1=request.user) | Q(user_2=request.user)
        ).order_by("-created_date")
        if not match:
            return failure_response("Match does not exist", status.HTTP_404_NOT_FOUND)
        return success_response(
            MatchSerializer(match[0], user=request.user).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Update current match for current user."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        match = Match.objects.filter(
            Q(user_1=request.user) | Q(user_2=request.user)
        ).order_by("-created_date")
        if match:
            return UpdateMatchController(
                match[0].id, request.user, data, self.serializer_class
            ).process()
        return failure_response("Match does not exist", status.HTTP_404_NOT_FOUND)


class CancelCurrentMatchView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Cancel current user's current match."""
        match = Match.objects.filter(
            Q(user_1=request.user) | Q(user_2=request.user)
        ).order_by("-created_date")
        if not match:
            return failure_response("Match does not exist", status.HTTP_404_NOT_FOUND)
        match = match[0]
        match.status = match_status.CANCELED
        match.save()
        return success_response()


class AlgorithmView(generics.GenericAPIView):
    permission_classes = api_settings.ADMIN_PERMISSIONS

    def get(self, request):
        """Run algorithm and return matches."""
        return success_response(
            data=pear_algorithm(
                User.objects.filter(
                    person__has_onboarded=True,
                    person__is_paused=False,
                )
            ),
            status=status.HTTP_201_CREATED,
        )

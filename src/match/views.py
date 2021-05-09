import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from django.db.models import Q
from match import match_status
from match.models import Match
from match.serializers import BothUsersMatchSerializer
from match.serializers import MatchSerializer
from rest_framework import generics

from .controllers.create_match_controller import CreateMatchController
from .controllers.update_match_controller import UpdateMatchController


class MatchesView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all matches."""
        matches = Match.objects.all().order_by("-created_date")
        return success_response(self.serializer_class(matches, many=True).data)

    def post(self, request):
        """Create a match."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateMatchController(data, self.serializer_class).process()


class MatchView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get match by id."""
        match = Match.objects.filter(id=id)
        if match:
            return success_response(self.serializer_class(match[0]).data)
        return failure_response("Match does not exist")

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
            return failure_response("Match does not exist")
        match[0].delete()
        return success_response()


class CancelMatchView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request, id):
        """Cancel match by id."""
        match = Match.objects.filter(id=id)
        if not match:
            return failure_response("Match does not exist.")
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
            return failure_response("Match does not exist")
        return success_response(MatchSerializer(match[0], user=request.user).data)

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
        return failure_response("Match does not exist")


class CancelCurrentMatchView(generics.GenericAPIView):
    serializer_class = BothUsersMatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def post(self, request):
        """Cancel current user's current match."""
        match = Match.objects.filter(
            Q(user_1=request.user) | Q(user_2=request.user)
        ).order_by("-created_date")
        if not match:
            return failure_response("Match does not exist")
        match = match[0]
        match.status = match_status.CANCELED
        match.save()
        return success_response()

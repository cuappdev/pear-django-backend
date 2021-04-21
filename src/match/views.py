import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from match.models import Match
from match.serializers import MatchSerializer
from rest_framework import generics

from .controllers.create_match_controller import CreateMatchController
from .controllers.update_match_controller import UpdateMatchController


class MatchesView(generics.GenericAPIView):
    serializer_class = MatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all matches."""
        matches = Match.objects.all()
        return success_response(
            self.serializer_class(matches, user=request.user, many=True).data
        )

    def post(self, request):
        """Create a match."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateMatchController(request, data, self.serializer_class).process()


class MatchView(generics.GenericAPIView):
    serializer_class = MatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get match by id."""
        match = Match.objects.filter(id=id)
        if match:
            return success_response(
                self.serializer_class(match[0], user=request.user).data
            )
        return failure_response("Match does not exist")

    def post(self, request, id):
        """Update match by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateMatchController(id, request, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete a match by id."""
        match = Match.objects.filter(id=id)
        if match:
            match[0].delete()
            return success_response(
                self.serializer_class(match[0], user=request.user).data
            )
        return failure_response("Match does not exist")


class CurrentMatchView(generics.GenericAPIView):
    serializer_class = MatchSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get current match by user."""
        match = Match.objects.filter(id=id)
        if match:
            if request.user.id == 1:
                return success_response(
                    MatchSerializer(match[0], user=request.user).data
                )
            elif request.user.id == 2:
                return success_response(
                    MatchSerializer(match[0], user=request.user).data
                )
        return failure_response("Match does not exist")

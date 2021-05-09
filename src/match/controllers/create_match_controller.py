from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from match import match_status
from match.models import Match
from rest_framework import status


class CreateMatchController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        """Process a request to create a match."""
        match_ids = self._data.get("ids")
        if match_ids is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )
        user_1 = User.objects.filter(id=match_ids[0])
        user_2 = User.objects.filter(id=match_ids[1])
        if not user_1:
            return failure_response(f"User with id {match_ids[0]} does not exist")
        if not user_2:
            return failure_response(f"User with id {match_ids[1]} does not exist")
        user_1 = user_1[0]
        user_2 = user_2[0]
        possible_match_1 = Match.objects.filter(
            user_1=user_1, user_2=user_2, status=match_status.CREATED
        )
        possible_match_2 = Match.objects.filter(
            user_1=user_2, user_2=user_1, status=match_status.CREATED
        )
        if possible_match_1 or possible_match_2:
            return success_response(None, status.HTTP_200_OK)
        match = Match.objects.create(
            status=match_status.CREATED,
            user_1=user_1,
            user_2=user_2,
            accepted_ids=[],
            proposed_meeting_times="[]",
        )
        match.proposed_locations.set([])
        match.save()
        return success_response(None, status.HTTP_201_CREATED)

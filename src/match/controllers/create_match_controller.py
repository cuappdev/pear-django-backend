from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from django.db.models import Q
from match import match_status
from match.models import Match
from rest_framework import status


class CreateMatchController:
    def __init__(self, data, serializer, return_status=False):
        self._data = data
        self._serializer = serializer
        self._return_status = return_status  # Returns True if successful, otherwise False and error message

    def process(self):
        match_ids = self._data.get("ids")
        cancel_previous = self._data.get("cancel_previous", False)
        if match_ids is None:
            error_msg = "POST body is misformatted"
            return (
                (False, error_msg)
                if self._return_status
                else failure_response(error_msg, status.HTTP_400_BAD_REQUEST)
            )
        # Always set user_1 to the lower user id
        user_1 = User.objects.filter(id=min(match_ids)).exists()
        if not user_1:
            error_msg = f"User with id {min(match_ids)} does not exist"
            return (
                (False, error_msg)
                if self._return_status
                else failure_response(error_msg)
            )
        # Always set user_2 to the higher user id
        user_2 = User.objects.filter(id=max(match_ids)).exists()
        if not user_2:
            error_msg = f"User with id {max(match_ids)} does not exist"
            return (
                (False, error_msg)
                if self._return_status
                else failure_response(error_msg)
            )
        user_1 = User.objects.get(id=min(match_ids))
        user_2 = User.objects.get(id=max(match_ids))
        possible_match = Match.objects.filter(
            user_1=user_1, user_2=user_2, status=match_status.CREATED
        )
        if cancel_previous:
            user_1_previous_matches = Match.objects.filter(
                Q(user_1=user_1) | Q(user_2=user_1)
            )
            user_2_previous_matches = Match.objects.filter(
                Q(user_1=user_2) | Q(user_2=user_2)
            )
            user_1_previous_matches.update(status=match_status.CANCELED)
            user_2_previous_matches.update(status=match_status.CANCELED)
        if possible_match:
            return (
                (True, "")
                if self._return_status
                else success_response(None, status.HTTP_200_OK)
            )
        match = Match.objects.create(
            status=match_status.CREATED,
            user_1=user_1,
            user_2=user_2,
            accepted_ids=[],
            proposed_meeting_times="[]",
        )
        match.proposed_locations.set([])
        match.save()
        user_1.person.pending_feedback = True
        user_2.person.pending_feedback = True
        user_1.person.save()
        user_2.person.save()
        return (
            (True, "")
            if self._return_status
            else success_response(None, status.HTTP_201_CREATED)
        )

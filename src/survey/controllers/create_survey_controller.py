import json

from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from match import match_status
from match.models import Match
from rest_framework import status
from survey import constants
from survey.models import Survey


# TODO(@chalo2000) Convert to celery task
class CreateSurveyController:
    def __init__(self, request, data, match_id):
        self._request = request
        self._data = data
        self._match_id = match_id

    def process(self):
        # Verify that all required fields are provided
        did_meet = self._data.get("did_meet")
        if did_meet is None:
            return failure_response("did_meet", status.HTTP_400_BAD_REQUEST)

        # Get optional fields based on did_meet
        did_meet_reason = self._data.get("did_meet_reason")
        did_not_meet_reasons = self._data.get("did_not_meet_reasons")
        rating = self._data.get("rating")
        if did_meet:
            if rating is None:
                return failure_response(
                    "Rating is required for a completed match",
                    status.HTTP_400_BAD_REQUEST,
                )
            elif rating not in constants.RATINGS:
                return failure_response(
                    "The provided rating is invalid", status.HTTP_400_BAD_REQUEST
                )
        else:
            if not did_not_meet_reasons:
                return failure_response(
                    "did_not_meet_reasons is required if did_meet is False",
                    status.HTTP_400_BAD_REQUEST,
                )
            if not all(
                map(lambda x: x in constants.DID_NOT_MEET_LONG, did_not_meet_reasons)
            ):
                return failure_response(
                    "did_not_meet_reasons has invalid elements",
                    status.HTTP_400_BAD_REQUEST,
                )

            did_not_meet_reasons = list(
                map(lambda x: constants.long_to_short(x), did_not_meet_reasons)
            )
            if len(did_not_meet_reasons) > 5:
                return failure_response(
                    "Too many elements in did_not_meet_reasons",
                    status.HTTP_400_BAD_REQUEST,
                )

        # Verify that required ids are valid
        completed_match = Match.objects.filter(id=self._match_id)
        if not completed_match:
            return failure_response("match_id is invalid", status.HTTP_404_NOT_FOUND)
        completed_match = completed_match[0]

        # Check if the submitting user has already submitted a survey
        submitting_person = self._request.user.person
        survey = Survey.objects.filter(
            submitting_person=submitting_person, completed_match=completed_match
        )
        if survey:
            return failure_response(
                "This user has already submitted feedback to the provided match!",
                status.HTTP_403_FORBIDDEN,
            )

        # Update match status based on feedback
        if not did_meet:
            # Cancel a match if any person says they did not meet
            modify_attribute(completed_match, "status", match_status.CANCELED)
        # Force a match to stay canceled if set before
        # TODO(@team) Check how often this edge case fails through explanations
        elif completed_match.status != match_status.CANCELED:
            modify_attribute(completed_match, "status", match_status.INACTIVE)
        completed_match.save()

        # Create and return a new survey with the given fields
        survey = Survey.objects.create(
            did_meet=did_meet,
            did_meet_reason=did_meet_reason,
            did_not_meet_reasons=json.dumps(did_not_meet_reasons)
            if not did_meet
            else None,
            rating=rating,
            submitting_person=submitting_person,
            completed_match=completed_match,
        )
        submitting_person.pending_feedback = False
        survey.save()
        submitting_person.save()
        return success_response(None, status.HTTP_201_CREATED)

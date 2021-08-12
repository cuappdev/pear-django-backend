from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from match import match_status
from match.models import Match
from person.models import Person
from rest_framework import status
from survey.constants import RATINGS
from survey.models import Survey


# TODO(@chalo2000) Convert to celery task
class CreateSurveyController:
    def __init__(self, request, data):
        self._request = request
        self._data = data

    def process(self):
        # Verify that all required fields are provided
        did_meet = self._data.get("did_meet")
        explanation = self._data.get("explanation")
        completed_match_id = self._data.get("completed_match_id")
        if explanation is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        # Get optional fields
        rating = self._data.get("rating")
        if rating is not None and rating not in RATINGS:
            return failure_response(
                "The provided rating is invalid", status.HTTP_400_BAD_REQUEST
            )

        # Verify that required ids are valid
        completed_match = Match.objects.filter(id=completed_match_id)
        if not completed_match:
            return failure_response(
                "completed_match_id is invalid", status.HTTP_404_NOT_FOUND
            )
        completed_match = completed_match[0]

        # Check if the submitting user has already submitted a survey
        submitting_user = Person.objects.filter(id=self._request.user.id)[0]
        survey = Survey.objects.filter(
            submitting_user=submitting_user, completed_match=completed_match
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
            explanation=explanation,
            rating=rating,
            submitting_user=submitting_user,
            completed_match=completed_match,
        )
        survey.save()
        return success_response(None, status.HTTP_201_CREATED)

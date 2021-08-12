from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from rest_framework import status
from survey.constants import RATINGS
from survey.models import Survey


# TODO(@chalo2000) Convert to celery task
class UpdateSurveyController:
    def __init__(self, id, data):
        self._id = id
        self._data = data

    def process(self):
        # Get the model
        survey = Survey.objects.filter(id=self._id)
        if survey is None:
            return failure_response("Survey does not exist", status.HTTP_404_NOT_FOUND)
        survey = survey[0]

        # Extract attributes
        did_meet = self._data.get("did_meet")
        explanation = self._data.get("explanation")
        rating = self._data.get("rating")
        if rating is not None and rating not in RATINGS:
            return failure_response(
                "The provided rating is invalid", status.HTTP_400_BAD_REQUEST
            )

        # Modify new fields
        modify_attribute(survey, "did_meet", did_meet)
        modify_attribute(survey, "explanation", explanation)
        modify_attribute(survey, "rating", rating)

        survey.save()
        return success_response(None, status.HTTP_200_OK)

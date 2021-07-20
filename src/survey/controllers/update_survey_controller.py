from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from rest_framework import status
from survey.models import Survey


class UpdateSurveyController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        # Get the model
        survey = Survey.objects.filter(id=self._id)
        if survey is None:
            return failure_response("Survey does not exist", status.HTTP_404_NOT_FOUND)
        survey = survey[0]

        # Extract attributes
        explanation = self._data.get("explanation")
        rating = self._data.get("rating")

        # Modify new fields
        modify_attribute(survey, "explanation", explanation)
        modify_attribute(survey, "rating", rating)

        survey.save()
        return success_response(self._serializer(survey).data, status.HTTP_200_OK)

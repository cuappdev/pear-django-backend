from api.utils import failure_response
from api.utils import success_response
from rest_framework import status
from survey.models import Survey


class CreateSurveyController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        # Verify that all required fields are provided
        explanation = self._data.get("explanation")
        if explanation is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        # Get optional fields
        rating = self._data.get("rating")

        # Check if a survey already exists with the given fields and return it if so
        survey = Survey.objects.filter(explanation=explanation, rating=rating)
        if survey:
            return success_response(
                self._serializer(survey[0]).data, status.HTTP_200_OK
            )

        # Create and return a new survey with the given fields
        survey = Survey.objects.create(explanation=explanation, rating=rating)
        survey.save()
        return success_response(self._serializer(survey).data, status.HTTP_201_CREATED)

import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from rest_framework import generics
from rest_framework import status
from survey.models import Survey

from .controllers.create_survey_controller import CreateSurveyController
from .controllers.update_survey_controller import UpdateSurveyController
from .serializers import SurveySerializer


class SurveysView(generics.GenericAPIView):
    serializer_class = SurveySerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all surveys."""
        surveys = Survey.objects.all()
        return success_response(
            self.serializer_class(surveys, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create a survey."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateSurveyController(data, self.serializer_class).process()


class SurveyView(generics.GenericAPIView):
    serializer_class = SurveySerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get survey by id."""
        survey = Survey.objects.filter(id=id)
        if not survey:
            return failure_response("Survey does not exist", status.HTTP_404_NOT_FOUND)
        return success_response(
            self.serializer_class(survey[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update survey by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateSurveyController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete a survey by id."""
        survey = Survey.objects.filter(id=id)
        if not survey:
            return failure_response("Survey does not exist", status.HTTP_404_NOT_FOUND)
        survey[0].delete()
        return success_response(
            self.serializer_class(survey[0]).data, status.HTTP_200_OK
        )

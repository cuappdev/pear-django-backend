import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from purpose.models import Purpose
from rest_framework import generics
from rest_framework import status

from .controllers.create_purpose_controller import CreatePurposeController
from .controllers.update_purpose_controller import UpdatePurposeController
from .serializers import PurposeSerializer


class PurposesView(generics.GenericAPIView):
    serializer_class = PurposeSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all purposes."""
        purposes = Purpose.objects.all()
        return success_response(
            self.serializer_class(purposes, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create a purpose."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreatePurposeController(data, self.serializer_class).process()


class PurposeView(generics.GenericAPIView):
    serializer_class = PurposeSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get purpose by id."""
        purpose = Purpose.objects.filter(id=id)
        if not purpose:
            return failure_response("Purpose does not exist", status.HTTP_404_NOT_FOUND)
        return success_response(
            self.serializer_class(purpose[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update purpose by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdatePurposeController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete a purpose by id."""
        purpose = Purpose.objects.filter(id=id)
        if not purpose:
            return failure_response("Purpose does not exist", status.HTTP_404_NOT_FOUND)
        purpose[0].delete()
        return success_response(
            self.serializer_class(purpose[0]).data, status.HTTP_200_OK
        )

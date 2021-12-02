import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from major.models import Major
from rest_framework import generics
from rest_framework import status

from .controllers.create_major_controller import CreateMajorController
from .controllers.update_major_controller import UpdateMajorController
from .serializers import MajorSerializer


class MajorsView(generics.GenericAPIView):
    serializer_class = MajorSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all majors."""
        majors = Major.objects.all()
        return success_response(
            self.serializer_class(majors, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create a major."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateMajorController(data, self.serializer_class).process()


class MajorView(generics.GenericAPIView):
    serializer_class = MajorSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get major by id."""
        major = Major.objects.filter(id=id)
        if not major:
            return failure_response("Major does not exist", status.HTTP_404_NOT_FOUND)
        return success_response(
            self.serializer_class(major[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update major by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateMajorController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete a major by id."""
        major = Major.objects.filter(id=id)
        if not major:
            return failure_response("Major does not exist", status.HTTP_404_NOT_FOUND)
        major[0].delete()
        return success_response(
            self.serializer_class(major[0]).data, status.HTTP_200_OK
        )

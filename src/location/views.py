import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from rest_framework import generics
from rest_framework import status

from .controllers.create_location_controller import CreateLocationController
from .controllers.update_location_controller import UpdateLocationController
from .serializers import LocationSerializer


class LocationsView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all locations."""
        locations = Location.objects.all()
        return success_response(
            self.serializer_class(locations, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create a location."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateLocationController(data, self.serializer_class).process()


class LocationView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get location by id."""
        location = Location.objects.filter(id=id)
        if not location:
            return failure_response(
                "Location does not exist", status.HTTP_404_NOT_FOUND
            )
        return success_response(
            self.serializer_class(location[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update location by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateLocationController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete a location by id."""
        location = Location.objects.filter(id=id)
        if not location:
            return failure_response(
                "Location does not exist", status.HTTP_404_NOT_FOUND
            )
        location[0].delete()
        return success_response(
            self.serializer_class(location[0]).data, status.HTTP_200_OK
        )

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from rest_framework import generics
from rest_framework import status

from .controllers.create_location_controller import CreateLocationController
from .serializers import LocationSerializer


class LocationsView(generics.GenericAPIView):
    serializer_class = LocationSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all locations."""
        locations = Location.objects.all()
        return success_response(self.serializer_class(locations, many=True).data)

    def post(self, request):
        """Create a location."""
        return CreateLocationController(
            request=request, serializer=self.serializer_class
        ).process()

    def delete(self, request):
        """Delete a location."""
        data = request.data
        name = data.get("name")
        if name is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )
        location = Location.objects.filter(name=name)
        if location:
            location[0].delete()
        else:
            return failure_response("Provided location does not exist")
        return success_response(self.serializer_class(location[0]).data)

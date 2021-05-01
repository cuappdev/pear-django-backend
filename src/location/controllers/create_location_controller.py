from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from rest_framework import status


class CreateLocationController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        # Verify that all required fields are provided
        name = self._data.get("name")
        area = self._data.get("area")
        if name is None or area is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        # Check if a location already exists with the given fields and return it if so
        location = Location.objects.filter(name=name, area=area)
        if location:
            return success_response(
                self._serializer(location[0]).data, status.HTTP_200_OK
            )

        # Create and return a new location with the given fields
        location = Location.objects.create(name=name, area=area)
        location.save()
        return success_response(
            self._serializer(location).data, status.HTTP_201_CREATED
        )

from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from location.models import Location
from rest_framework import status


class UpdateLocationController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        # Get the model
        location = Location.objects.filter(id=self._id)
        if location is None:
            return failure_response(
                "Location does not exist", status.HTTP_404_NOT_FOUND
            )
        location = location[0]

        # Extract attributes
        area = self._data.get("area")
        name = self._data.get("name")

        # Modify new fields
        modify_attribute(location, "area", area)
        modify_attribute(location, "name", name)

        # Save new changes
        location.save()
        return success_response(self._serializer(location).data, status.HTTP_200_OK)

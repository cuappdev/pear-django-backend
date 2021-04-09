import json

from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from rest_framework import status


class UpdateLocationController:
    def __init__(self, location_id, request, data, serializer):
        self._location_id = location_id
        self._request = request
        self._serializer = serializer
        self._data = data

    def process(self):
        """Process a request to update a location's fields that have changed.
        The possible status code cases for a processed request include
        - 201 if the location was successfully updated
          - Returns the updated Location
        - 400 if the POST body is misformatted
          - Returns an error message"""
        self._body = json.loads(self._request.body)
        name = self._body.get("name")
        area = self._body.get("area")
        location = Location.objects.filter(id=self._location_id)
        if not location:
            return failure_response("Location does not exist")

        if name is not None and location[0].name != name:
            location[0].name = name
        if area is not None and location[0].area != area:
            location[0].area = area

        location[0].save()
        return success_response(self._serializer(location[0]).data, status.HTTP_200_OK)

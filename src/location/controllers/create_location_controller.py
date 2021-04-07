import json

from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from rest_framework import status


class CreateLocationController:
    def __init__(self, request=None, serializer=None, data=None):
        self._request = request
        self._serializer = serializer
        self._data = data

    def _process_request(self):
        """The possible status code cases for a processed request include
        - 200 if the request body describes an existing Location
          - Returns the existing Location
        - 201 if the request body describes a new Location or updates the area for a Location
          - Creates and then returns the new (or existing) Location
        - 400 if the POST body is misformatted
          - Returns an error message"""
        self._body = json.loads(self._request.body)
        name = self._body.get("name")
        area = self._body.get("area")
        if name is None or area is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )
        location = Location.objects.filter(name=name)
        if location and location[0].area != area:
            location[0].area = area
            location[0].save()
            return success_response(
                self._serializer(location[0]).data, status.HTTP_201_CREATED
            )
        elif location:
            location = location[0]
            return success_response(self._serializer(location).data, status.HTTP_200_OK)
        else:
            location = Location.objects.create(name=name, area=area)
            location.save()
            return success_response(
                self._serializer(location).data, status.HTTP_201_CREATED
            )

    def _process_data(self):
        """Returns True after creating a Location if the datum in the
        data describes a unique Location"""
        name = self._data[1]
        area = self._data[0]
        location = Location.objects.filter(name=name)
        if location and location[0].area != area:
            location[0].area = area
            location[0].save()
            return True
        elif location:
            return False
        else:
            location = Location.objects.create(name=name, area=area)
            location.save()
            return True

    def process(self):
        if self._request:
            return self._process_request()
        elif self._data:
            return self._process_data()

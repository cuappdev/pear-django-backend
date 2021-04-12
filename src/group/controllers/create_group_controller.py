import json

from api.utils import failure_response
from api.utils import success_response
from group.models import Group
from rest_framework import status


class CreateGroupController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._serializer = serializer
        self._data = data

    def process(self):
        """Process a request to create a group.
        The possible status code cases for a processed request include
        - 200 if the request body describes an existing Group
          - Returns the existing Group
        - 201 if the request body describes a new Group or updates the area for a Group
          - Creates and then returns the new (or existing) Group
        - 400 if the POST body is misformatted
          - Returns an error message"""
        self._body = json.loads(self._request.body)
        name = self._body.get("name")
        if name is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )
        group = Group.objects.filter(name=name)
        if group:
            return success_response(self._serializer(group[0]).data, status.HTTP_200_OK)
        group = Group.objects.create(name=name)
        group.save()
        return success_response(self._serializer(group).data, status.HTTP_201_CREATED)

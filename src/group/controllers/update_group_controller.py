import json

from api.utils import failure_response
from api.utils import success_response
from group.models import Group
from rest_framework import status


class UpdateGroupController:
    def __init__(self, group_id, request, data, serializer):
        self._group_id = group_id
        self._request = request
        self._serializer = serializer
        self._data = data

    def process(self):
        """Process a request to update a group's fields that have changed.
        The possible status code cases for a processed request include
        - 201 if the group was successfully updated
          - Returns the updated Group
        - 400 if the POST body is misformatted
          - Returns an error message"""
        self._body = json.loads(self._request.body)
        name = self._body.get("name")
        group = Group.objects.filter(id=self._group_id)
        if not group:
            return failure_response("Group does not exist")
        if name is not None and group[0].name != name:
            group[0].name = name
        group[0].save()
        return success_response(self._serializer(group[0]).data, status.HTTP_200_OK)

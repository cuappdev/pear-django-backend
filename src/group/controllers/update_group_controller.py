from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from group.models import Group
from rest_framework import status


class UpdateGroupController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        # Get the model
        group = Group.objects.filter(id=self._id)
        if group is None:
            return failure_response("Group does not exist", status.HTTP_404_NOT_FOUND)
        group = group[0]

        # Extract attributes
        name = self._data.get("name")
        subtitle = self._data.get("subtitle")
        img_url = self._data.get("img_url")

        # Modify new fields
        modify_attribute(group, "name", name)
        modify_attribute(group, "subtitle", subtitle)
        modify_attribute(group, "img_url", img_url)

        # Save new changes
        group.save()
        return success_response(self._serializer(group).data, status.HTTP_200_OK)

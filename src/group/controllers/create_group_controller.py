from api.utils import failure_response
from api.utils import success_response
from group.models import Group
from rest_framework import status


class CreateGroupController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        """Process a request to create a group."""

        # Verify that all required fields are provided
        name = self._data.get("name")
        if name is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        # Get optional fields
        subtitle = self._data.get("subtitle")
        img_url = self._data.get("img_url")

        # Check if a group already exists with the given fields and return it if so
        group = Group.objects.filter(name=name, subtitle=subtitle, img_url=img_url)
        if group:
            return success_response(self._serializer(group[0]).data, status.HTTP_200_OK)

        # Create and return a new group with the given fields
        group = Group.objects.create(name=name, subtitle=subtitle, img_url=img_url)
        group.save()
        return success_response(self._serializer(group).data, status.HTTP_201_CREATED)

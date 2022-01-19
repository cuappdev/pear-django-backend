from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from purpose.models import Purpose
from rest_framework import status


class UpdatePurposeController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        # Get the model
        purpose = Purpose.objects.filter(id=self._id)
        if not purpose:
            return failure_response("Purpose does not exist", status.HTTP_404_NOT_FOUND)
        purpose = purpose[0]

        # Extract attributes
        name = self._data.get("name")

        # Modify new fields
        modify_attribute(purpose, "name", name)

        purpose.save()
        return success_response(self._serializer(purpose).data, status.HTTP_200_OK)

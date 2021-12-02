from api.utils import failure_response
from api.utils import success_response
from purpose.models import Purpose
from rest_framework import status


class CreatePurposeController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        # Verify that all required fields are provided
        name = self._data.get("name")
        if name is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        # Check if a purpose already exists with the given fields and return it if so
        purpose = Purpose.objects.filter(name=name)
        if purpose:
            return success_response(
                self._serializer(purpose[0]).data, status.HTTP_200_OK
            )

        # Create and return a new purpose with the given fields
        purpose = Purpose.objects.create(name=name)
        purpose.save()
        return success_response(self._serializer(purpose).data, status.HTTP_201_CREATED)

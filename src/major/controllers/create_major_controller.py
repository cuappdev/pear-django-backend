from api.utils import failure_response
from api.utils import success_response
from major.models import Major
from rest_framework import status


class CreateMajorController:
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

        # Check if a major already exists with the given fields and return it if so
        major = Major.objects.filter(name=name)
        if major:
            return success_response(self._serializer(major[0]).data, status.HTTP_200_OK)

        # Create and return a new major with the given fields
        major = Major.objects.create(name=name)
        major.save()
        return success_response(self._serializer(major).data, status.HTTP_201_CREATED)

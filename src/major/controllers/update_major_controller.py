from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from major.models import Major
from rest_framework import status


class UpdateMajorController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        # Get the model
        major = Major.objects.filter(id=self._id)
        if not major:
            return failure_response("Major does not exist", status.HTTP_404_NOT_FOUND)
        major = major[0]

        # Extract attributes
        name = self._data.get("name")

        # Modify new fields
        modify_attribute(major, "name", name)

        major.save()
        return success_response(self._serializer(major).data, status.HTTP_200_OK)

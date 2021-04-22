from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from interest.models import Interest
from rest_framework import status


class UpdateInterestController:
    def __init__(self, id, data, serializer):
        self._id = id
        self._data = data
        self._serializer = serializer

    def process(self):
        """Process a request to update an interest's fields that have changed."""

        # Get the model
        interest = Interest.objects.filter(id=self._id)
        if interest is None:
            return failure_response(
                "Interest does not exist", status.HTTP_404_NOT_FOUND
            )
        interest = interest[0]

        # Extract attributes
        name = self._data.get("name")
        subtitle = self._data.get("subtitle")
        img_url = self._data.get("img_url")

        # Modify new fields
        modify_attribute(interest, "name", name)
        modify_attribute(interest, "subtitle", subtitle)
        modify_attribute(interest, "img_url", img_url)

        interest.save()
        return success_response(self._serializer(interest).data, status.HTTP_200_OK)

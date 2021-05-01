from api.utils import failure_response
from api.utils import success_response
from interest.models import Interest
from rest_framework import status


class CreateInterestController:
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

        # Get optional fields
        subtitle = self._data.get("subtitle")
        img_url = self._data.get("img_url")

        # Check if a interest already exists with the given fields and return it if so
        interest = Interest.objects.filter(
            name=name, subtitle=subtitle, img_url=img_url
        )
        if interest:
            return success_response(
                self._serializer(interest[0]).data, status.HTTP_200_OK
            )

        # Create and return a new interest with the given fields
        interest = Interest.objects.create(
            name=name, subtitle=subtitle, img_url=img_url
        )
        interest.save()
        return success_response(
            self._serializer(interest).data, status.HTTP_201_CREATED
        )

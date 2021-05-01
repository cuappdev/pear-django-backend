import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from interest.models import Interest
from rest_framework import generics
from rest_framework import status

from .controllers.create_interest_controller import CreateInterestController
from .controllers.update_interest_controller import UpdateInterestController
from .serializers import InterestSerializer


class InterestsView(generics.GenericAPIView):
    serializer_class = InterestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all interests."""
        interests = Interest.objects.all()
        return success_response(
            self.serializer_class(interests, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create an interest."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateInterestController(data, self.serializer_class).process()


class InterestView(generics.GenericAPIView):
    serializer_class = InterestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get interest by id."""
        interest = Interest.objects.filter(id=id)
        if not interest:
            return failure_response(
                "Interest does not exist", status.HTTP_404_NOT_FOUND
            )
        return success_response(
            self.serializer_class(interest[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update interest by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateInterestController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete an interest by id."""
        interest = Interest.objects.filter(id=id)
        if not interest:
            return failure_response(
                "Interest does not exist", status.HTTP_404_NOT_FOUND
            )
        interest[0].delete()
        return success_response(
            self.serializer_class(interest[0]).data, status.HTTP_200_OK
        )

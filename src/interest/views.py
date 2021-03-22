import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from interest.models import Interest
from rest_framework import generics
from rest_framework import status as s

from .serializers import InterestSerializer


class InterestAllView(generics.GenericAPIView):
    serializer_class = InterestSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """ Get all interests """
        interests = Interest.objects.all()
        return success_response(self.serializer_class(interests, many=True).data)

    def post(self, request):
        """ Create an interest """
        try:
            body = json.loads(request.body)
            name = body.get("name")
            assert name
        except:
            return failure_response("POST body is misformatted", s.HTTP_400_BAD_REQUEST)
        interest = Interest.objects.filter(name=name)
        if interest:
            interest = interest[0]
            status = s.HTTP_200_OK
        else:
            interest = Interest.objects.create(name=name)
            interest.save()
            status = s.HTTP_201_CREATED
        return success_response(self.serializer_class(interest).data, status=status)

    def delete(self, request):
        """ Delete an interest """
        try:
            body = json.loads(request.body)
            name = body.get("name")
            assert name
        except:
            return failure_response("POST body is misformatted", s.HTTP_400_BAD_REQUEST)
        interest = Interest.objects.filter(name=name)
        if interest:
            interest[0].delete()
        else:
            return failure_response("Provided interest does not exist")
        return success_response(self.serializer_class(interest[0]).data)

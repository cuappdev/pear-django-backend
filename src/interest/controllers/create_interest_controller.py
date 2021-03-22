import json

from api.utils import failure_response
from api.utils import success_response
from interest.models import Interest
from rest_framework import status as s


class CreateInterestController:
    def __init__(self, request=None, serializer=None, data=None):
        self._request = request
        self._serializer = serializer
        self._data = data

    def _process_request(self):
        """The possible status code cases for a processed request include
        - 200 if the request body describes an existing Interest
          - Returns the existing Interest
        - 201 if the request body describes a new Interest
          - Creates and then returns the new Interest
        - 400 if the POST body is misformatted
          - Returns an error message
        """
        try:
            body = json.loads(self._request.body)
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
        return success_response(self._serializer(interest).data, status=status)

    def _process_data(self):
        """Returns True after creating an Interest if the datum in the
        data describes a unique Interest \n
        PRECONDITION: `_data[0]` is `name`"""
        name = self._data[0]
        interest = Interest.objects.filter(name=name)
        if interest:
            return False
        else:
            interest = Interest.objects.create(name=name)
            interest.save()
            return True

    def process(self):
        if self._request:
            return self._process_request()
        elif self._data:
            return self._process_data()

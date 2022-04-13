from api.utils import success_response
from django.utils import timezone
from rest_framework import status


class PingPersonController:
    def __init__(self, user, data, serializer):
        self._data = data
        self._serializer = serializer
        self._user = user
        self._person = self._user.person

    def process(self):
        self._person.last_active = timezone.now()
        self._user.save()
        self._person.save()
        return success_response(status=status.HTTP_200_OK)

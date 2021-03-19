from django.shortcuts import render
import json

from api import settings as api_settings
from api.utils import success_response
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics

from .controllers.authenticate_controller import AuthenticateController
from .serializers import AuthenticateSerializer

# Create your views here.
class AuthenticateView(generics.GenericAPIView):
    serializer_class = AuthenticateSerializer
    permission_classes = api_settings.UNPROTECTED

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return AuthenticateController(request, data, self.serializer_class).process()

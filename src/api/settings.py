import os

from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin

ADMIN_PERMISSIONS = [IsAuthenticated, IsAdmin]

STANDARD_PERMISSIONS = [IsAuthenticated, DjangoModelPermissions]

CONSUMER_PERMISSIONS = [IsAuthenticated]

UNPROTECTED = [AllowAny]


AUTH_PASSWORD_SALT = os.getenv("AUTH_PASSWORD_SALT")
ACCESS_TOKEN_AGE = 60 * 15  # 15 minutes
GOOGLE_DEBUG = os.getenv("GOOGLE_DEBUG") == "True"

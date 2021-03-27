from rest_framework.permissions import AllowAny
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin

ADMIN_PERMISSIONS = [IsAuthenticated, IsAdmin]

STANDARD_PERMISSIONS = [IsAuthenticated, DjangoModelPermissions]

CONSUMER_PERMISSIONS = [IsAuthenticated]

UNPROTECTED = [AllowAny]

AUTH_PASSWORD_SALT = "LtC66ubP"
ACCESS_TOKEN_AGE = 60 * 15  # 15 minutes

UPLOAD_URL = "https://upload.cornellappdev.com/upload/"

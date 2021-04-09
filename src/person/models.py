from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    net_id = models.CharField(max_length=10)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, default=None
    )
    hometown = models.CharField(max_length=50, default=None, null=True)
    profile_pic_url = models.CharField(max_length=100, default=None, null=True)
    facebook_url = models.CharField(max_length=50, default=None, null=True)
    instagram_username = models.CharField(max_length=30, default=None, null=True)
    graduation_year = models.CharField(max_length=4, default=None, null=True)
    pronouns = models.CharField(max_length=20, default=None, null=True)

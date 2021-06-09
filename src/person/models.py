from django.contrib.auth.models import User
from django.db import models
from group.models import Group
from interest.models import Interest
from location.models import Location
from major.models import Major


class Person(models.Model):
    net_id = models.CharField(max_length=10)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, default=None
    )
    hometown = models.CharField(max_length=50, default=None, null=True)
    majors = models.ManyToManyField(Major, default=None, blank=True)
    profile_pic_url = models.CharField(max_length=100, default=None, null=True)
    facebook_url = models.CharField(max_length=100, default=None, null=True)
    instagram_username = models.CharField(max_length=30, default=None, null=True)
    graduation_year = models.CharField(max_length=4, default=None, null=True)
    pronouns = models.CharField(max_length=20, default=None, null=True)
    goals = models.TextField(default=None, null=True)
    talking_points = models.TextField(default=None, null=True)
    availability = models.TextField(default=None, null=True)
    locations = models.ManyToManyField(Location, default=None, blank=True)
    interests = models.ManyToManyField(Interest, default=None, blank=True)
    groups = models.ManyToManyField(Group, default=None, blank=True)
    has_onboarded = models.BooleanField(default=False, null=True)

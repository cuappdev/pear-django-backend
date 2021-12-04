from django.contrib.auth.models import User
from django.db import models
from group.models import Group
from interest.models import Interest
from location.models import Location
from major.models import Major
from prompt.models import Prompt
from purpose.models import Purpose


class Person(models.Model):
    net_id = models.CharField(max_length=15)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, default=None
    )
    hometown = models.CharField(max_length=50, default=None, null=True)
    majors = models.ManyToManyField(Major, default=None, blank=True)
    profile_pic_url = models.CharField(max_length=100, default=None, null=True)
    facebook_url = models.CharField(max_length=100, default=None, null=True)
    instagram_username = models.CharField(max_length=30, default=None, null=True)
    graduation_year = models.CharField(max_length=20, default=None, null=True)
    pronouns = models.CharField(max_length=20, default=None, null=True)
    goals = models.TextField(default=None, null=True)
    talking_points = models.TextField(default=None, null=True)
    availability = models.TextField(default=None, null=True)
    locations = models.ManyToManyField(Location, default=None, blank=True)
    interests = models.ManyToManyField(Interest, default=None, blank=True)
    groups = models.ManyToManyField(Group, default=None, blank=True)
    prompt_questions = models.ManyToManyField(Prompt, default=None, blank=True)
    prompt_answers = models.TextField(default=None, null=True)
    has_onboarded = models.BooleanField(default=False)
    pending_feedback = models.BooleanField(default=False)
    purposes = models.ManyToManyField(Purpose, default=None, blank=True)
    soft_deleted = models.BooleanField(default=False)
    fcm_registration_token = models.TextField(default=None, null=True)
    matching_paused = models.BooleanField(default=False)

from django.contrib.auth.models import User
from django.db import models
from location.models import Location


class Match(models.Model):
    status = models.CharField(max_length=20)
    user_1 = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        related_name="matches_1",
    )
    user_2 = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        related_name="matches_2",
    )
    proposer_id = models.IntegerField(default=None, null=True)
    accepted_ids = models.CharField(
        default=None,
        null=True,
        max_length=10,
    )
    proposed_meeting_times = models.TextField(default="[]", null=True)
    proposed_locations = models.ManyToManyField(
        Location, default=None, related_name="matches_proposed"
    )
    meeting_location = models.ForeignKey(
        Location,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        related_name="matches_confirmed",
    )
    meeting_time = models.CharField(max_length=40, default=None, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

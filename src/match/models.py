from django.contrib.auth.models import User
from django.db import models
from location.models import Location
from match.validators import validate_int_list
from match.validators import validate_times_list


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
        validators=[validate_int_list],
        max_length=10,
    )
    proposed_meeting_times = models.TextField(
        default="[]", null=True, validators=[validate_times_list]
    )
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

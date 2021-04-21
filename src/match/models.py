from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from location.models import Location


class Match(models.Model):
    status = models.CharField(max_length=20)
    user_1 = models.ForeignKey(
        User, default=None, null=True, on_delete=models.CASCADE, related_name="+"
    )
    user_2 = models.ForeignKey(
        User, default=None, null=True, on_delete=models.CASCADE, related_name="+"
    )
    proposer_id = models.IntegerField(default=None, null=True)
    accepted_ids = models.CharField(
        default=None,
        null=True,
        validators=[validate_comma_separated_integer_list],
        max_length=10,
    )
    proposed_meeting_times = models.TextField(default=None, null=True)
    proposed_locations = models.ManyToManyField(
        Location, default=None, related_name="+"
    )
    meeting_location = models.ForeignKey(
        Location, default=None, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    meeting_time = models.CharField(max_length=40, default=None, null=True)

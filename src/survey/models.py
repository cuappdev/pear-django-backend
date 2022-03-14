from django.db import models
from match.models import Match
from person.models import Person


class Survey(models.Model):
    did_meet = models.BooleanField(default=None, null=True)
    did_meet_reason = models.TextField(default=None, null=True)
    rating = models.IntegerField(default=None, null=True)
    submitting_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    completed_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    did_not_meet_reasons = models.CharField(max_length=30, default=None, null=True)

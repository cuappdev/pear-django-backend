from django.db import models
from match.models import Match
from person.models import Person


class Survey(models.Model):
    explanation = models.TextField(default=None)
    rating = models.IntegerField(default=None, null=True)
    submitting_user = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    completed_match = models.ForeignKey(Match, on_delete=models.CASCADE)

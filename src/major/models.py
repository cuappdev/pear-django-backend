from django.db import models


class Major(models.Model):
    name = models.CharField(max_length=100)

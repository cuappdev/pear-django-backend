from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
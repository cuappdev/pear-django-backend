from django.db import models


class Purpose(models.Model):
    name = models.CharField(max_length=100)

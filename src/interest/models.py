from django.db import models


class Interest(models.Model):
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, default=None, null=True)
    img_url = models.CharField(max_length=100, default=None, null=True)

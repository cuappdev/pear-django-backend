from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    id_token = models.TextField(null=True)
    net_id = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
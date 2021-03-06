# Generated by Django 3.1.5 on 2021-06-05 21:35

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("location", "0001_initial"),
        ("group", "0002_auto_20210422_0339"),
        ("interest", "0002_auto_20210422_0819"),
        ("person", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="facebook_url",
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="groups",
            field=models.ManyToManyField(blank=True, default=None, to="group.Group"),
        ),
        migrations.AlterField(
            model_name="person",
            name="interests",
            field=models.ManyToManyField(
                blank=True, default=None, to="interest.Interest"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="locations",
            field=models.ManyToManyField(
                blank=True, default=None, to="location.Location"
            ),
        ),
    ]

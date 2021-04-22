# Generated by Django 3.1.5 on 2021-04-21 22:28

from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion
import match.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("location", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.CharField(max_length=20)),
                ("proposer_id", models.IntegerField(default=None, null=True)),
                (
                    "accepted_ids",
                    models.CharField(
                        default=None,
                        max_length=10,
                        null=True,
                        validators=[match.validators.validate_int_list],
                    ),
                ),
                (
                    "proposed_meeting_times",
                    models.TextField(
                        default=None,
                        null=True,
                        validators=[match.validators.validate_times_list],
                    ),
                ),
                (
                    "meeting_time",
                    models.CharField(default=None, max_length=40, null=True),
                ),
                (
                    "meeting_location",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="location.location",
                    ),
                ),
                (
                    "proposed_locations",
                    models.ManyToManyField(
                        default=None,
                        related_name="_match_proposed_locations_+",
                        to="location.Location",
                    ),
                ),
                (
                    "user_1",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_2",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

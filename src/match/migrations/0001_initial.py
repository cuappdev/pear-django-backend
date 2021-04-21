# Generated by Django 3.1.5 on 2021-04-14 07:47

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("location", "0001_initial"),
        ("person", "0015_remove_person_id_token"),
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
                ("proposed_meeting_times", models.TextField(default=None, null=True)),
                (
                    "meeting_time",
                    models.CharField(default=None, max_length=40, null=True),
                ),
                (
                    "meeting_location",
                    models.OneToOneField(
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
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="person.person",
                    ),
                ),
                (
                    "user_2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="person.person",
                    ),
                ),
            ],
        ),
    ]

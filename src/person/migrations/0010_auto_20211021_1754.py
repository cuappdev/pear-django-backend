# Generated by Django 3.1.5 on 2021-10-21 17:54

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0009_person_purposes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="net_id",
            field=models.CharField(max_length=15),
        ),
    ]

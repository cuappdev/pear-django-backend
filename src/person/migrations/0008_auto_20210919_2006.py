# Generated by Django 3.1.5 on 2021-09-19 20:06

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0007_auto_20210720_1949"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="graduation_year",
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]

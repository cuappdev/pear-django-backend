# Generated by Django 3.1.5 on 2021-03-21 02:28

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0003_auto_20210321_0227"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="facebook_url",
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]

# Generated by Django 3.1.5 on 2021-03-21 02:30

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0005_auto_20210321_0229"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="facebook_url",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
# Generated by Django 3.1.5 on 2021-11-12 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("person", "0012_auto_20211112_0627"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="fcm_device",
        ),
    ]
# Generated by Django 3.1.5 on 2021-08-06 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("prompt", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="prompt",
            old_name="label_users_see",
            new_name="question_placeholder",
        ),
    ]
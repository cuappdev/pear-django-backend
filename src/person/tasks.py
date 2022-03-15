import datetime
import os

from celery import shared_task
from django.contrib.auth.models import User
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask
from person.models import Person
import requests


@shared_task
def upload_profile_pic(user_id, profile_pic_base64):
    """Uploads image to AppDev Upload service, and modifies Person's profile_pic_url if successful."""
    request_body = {
        "bucket": os.environ.get("UPLOAD_BUCKET_NAME"),
        "image": profile_pic_base64,
    }
    response = requests.post(os.environ.get("IMAGE_UPLOAD_URL"), json=request_body)
    if response:
        user = User.objects.get(id=user_id)
        user.person.profile_pic_url = response.json().get("data")
        user.save()
        user.person.save()


@shared_task
def update_paused_users():
    expired_users = Person.objects.filter(pause_expiration__lt=datetime.datetime.now())
    expired_users.update(is_paused=False, pause_expiration=None)
    return f"Unpaused {len(expired_users)} users"


schedule, _ = IntervalSchedule.objects.get_or_create(
    every=5,
    period=IntervalSchedule.SECONDS,
)
PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Pause Pear Updater",
    task="person.tasks.update_paused_users",
)

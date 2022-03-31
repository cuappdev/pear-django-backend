import os

from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
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
    expired_users = Person.objects.filter(pause_expiration__lt=timezone.now())
    expired_users.update(is_paused=False, pause_expiration=None)


schedule, _ = IntervalSchedule.objects.get_or_create(
    every=12,
    period=IntervalSchedule.HOURS,
)


PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Pause Pear Updater",
    task="person.tasks.update_paused_users",
)

# TODO Uncomment when ready to unpause users after inactivity
# @shared_task
# def update_inactive_users():
#     three_weeks_ago = timezone.now() - timedelta(days=21)
#     inactive_users = Person.objects.filter(last_active__lt=three_weeks_ago)
#     inactive_users.update(is_paused=True, pause_expiration=None)


# PeriodicTask.objects.get_or_create(
#     interval=schedule,
#     name="Inactive User Updater",
#     task="person.tasks.update_inactive_users",
# )

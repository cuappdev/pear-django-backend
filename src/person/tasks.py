import os

from celery import shared_task
from django.contrib.auth.models import User
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

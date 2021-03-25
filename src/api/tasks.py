import time

from celery import shared_task


@shared_task
def start_countdown(seconds):
    time.sleep(seconds)
    print(f"{seconds} seconds later...")

import time

from celery import shared_task

count = 0


@shared_task
def start_countdown(seconds):
    time.sleep(seconds)
    print(f"{seconds} seconds later...")

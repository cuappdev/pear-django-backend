import datetime
import importlib

from celery import shared_task
from django.contrib.auth.models import User
from django.db.models import Q
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask
from match import match_status
from match.controllers.create_match_controller import CreateMatchController
from match.models import Match

algorithm = importlib.import_module("pear-algorithm.src.main.main")

# PROOF OF CONCEPT

schedule, _ = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES,
)


@shared_task
def update_noah():
    noah = User.objects.get(person__net_id="njs99")
    noah.last_name = "Solomon " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    noah.save()
    return "Saved Noah"


PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Update Noah",
    task="match.tasks.update_noah",
)

# END PROOF OF CONCEPT

# TODO: Test above schedule on dev w/ more users to see if this works,
#  eventually change to task below


@shared_task
def matcher():
    # Cancel previous matches that were not completed
    unfinished_matches = Match.objects.all().exclude(
        status__in=[match_status.CANCELED, match_status.INACTIVE]
    )
    unfinished_matches.update(status=match_status.CANCELED)

    # Generate pears
    users = User.objects.filter(
        Q(person__has_onboarded=True) & Q(person__soft_deleted=False)
    )
    pears = algorithm.main(users)
    match_creator = CreateMatchController(None, None, return_status=True)

    # Create new matches
    for pear in pears:
        match_creator._data = {"ids": pear}
        success, error_msg = match_creator.process()
        if not success:
            print(f"Match error between {pear}: {error_msg}")


# TODO: uncomment after proof of concept works on dev server
# PeriodicTask.objects.get_or_create(
#     crontab=schedule,
#     name="Matching Algorithm",
#     task="match.tasks.matcher",
# )

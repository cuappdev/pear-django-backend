from celery import shared_task
from django.contrib.auth.models import User
from django.db.models import Q
from match import match_status
from match.controllers.create_match_controller import CreateMatchController
from match.models import Match
from pear_algorithm.src.main import main as pear_algorithm

# from django_celery_beat.models import CrontabSchedule
# from django_celery_beat.models import PeriodicTask


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
    pears = pear_algorithm(users)
    match_creator = CreateMatchController(None, None, return_status=True)

    # Create new matches
    for pear in pears:
        match_creator._data = {"ids": pear}
        success, error_msg = match_creator.process()
        if not success:
            print(f"Match error between {pear}: {error_msg}")


# Commented out until we confirm the algorithm works on an endpoint
# schedule, _ = CrontabSchedule.objects.get_or_create(
#     minute="00", hour="16", day_of_week="7"
# )

# PeriodicTask.objects.get_or_create(
#     crontab=schedule,
#     name="Matching Algorithm",
#     task="match.tasks.matcher",
# )

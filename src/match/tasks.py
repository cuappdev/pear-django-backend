import datetime
import logging

from celery import Celery
from celery.signals import after_setup_logger
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask
from match.models import Match

# Get Pear algorithm
# current_dir = os.path.dirname(os.path.abspath(__file__))
# submodule_path = f"{current_dir}/../../pear-algorithm/src"
# sys.path.insert(0, submodule_path)
# from main import main

app = Celery()

# https://www.distributedpython.com/2018/08/28/celery-logging/
logger = logging.getLogger(__name__)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)


# @app.task
# def matcher():
#     # Cancel previous matches that were not completed. TODO verify this is what we want to do
#     today = timezone.now()
#     last_week = today - datetime.timedelta(
#         days=7
#     )  # should be before pears are released but after matching
#     previous_matches = Match.objects.filter(created_date__range=[last_week, today])
#     print(f"Previous: {previous_matches}")
#     unfinished_matches = previous_matches.exclude(
#         status__in=[match_status.CANCELED, match_status.INACTIVE]
#     )
#     print(f"Unfinished: {unfinished_matches}")
#     unfinished_matches.update(status=match_status.CANCELED)

#     # Generate pears
#     users = Person.objects.all()
#     pears = main(users, logger)
#     match_creator = CreateMatchController(None, None, return_status=True)

#     # Create new matches
#     for pear in pears:
#         match_creator._data = {"ids": pear}
#         success, error_msg = match_creator.process()
#         if not success:
#             print(f"Match error between {pear}: {error_msg}")


@app.task
def test():
    matches = Match.objects.filter(created_date__lt=datetime.datetime.now())
    return matches.first().id


schedule, _ = IntervalSchedule.objects.get_or_create(
    every=5,
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Pear Algorithm",
    task="match.tasks.test",
)

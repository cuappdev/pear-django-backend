import logging

from celery import Celery
from celery.signals import after_setup_logger
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask

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


def dummy_scoring_algorithm():
    logger.warning("running dummy scoring algo")


def dummy_matching_algorithm():
    logger.warning("running dummy matching algo")


@app.task
def matcher():
    dummy_scoring_algorithm()
    dummy_matching_algorithm()


schedule, _ = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Matching Algorithm",
    task="match.tasks.matcher",
)

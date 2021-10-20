import logging
import os
import sys

from celery import Celery
from celery.signals import after_setup_logger
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask
from main import main

# Get Pear algorithm

current_dir = os.path.dirname(os.path.abspath(__file__))
submodule_path = f"{current_dir}/../../pear-algorithm/src"
sys.path.insert(0, submodule_path)

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


@app.task
def matcher():
    main(logger)


schedule, _ = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)

PeriodicTask.objects.get_or_create(
    interval=schedule,
    name="Pear Algorithm",
    task="match.tasks.matcher",
)

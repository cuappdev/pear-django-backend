import json

from api.utils import failure_response
from api.utils import success_response
from interest.controllers.create_interest_controller import CreateInterestController
from location.controllers.create_location_controller import CreateLocationController
from pear import settings as pear_settings
from rest_framework import generics
from rest_framework import status

from . import settings as api_settings
from .tasks import start_countdown


class PopulateView(generics.GenericAPIView):
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def _parse_and_create(self, filename, controller):
        """Parses `filename` and feeds each processed line to `controller`
        to be created into a new entry if not already in the database.
        Returns the number of newly created data entries."""
        newEntries = 0
        with open(f"{pear_settings.ASSETS_LOCATION}{filename}") as file:
            for line in file:
                line = line.strip().split(pear_settings.ASSETS_SPLITTER)
                newEntries += 1 if controller(data=line).process() else 0
        return newEntries

    def _filename_switch(self, filename):
        """Returns the appropriate controller class for `filename`."""
        switch = {
            "pear_groups.txt": None,  # TODO
            "pear_interests.txt": CreateInterestController,
            "pear_locations.txt": CreateLocationController,  # TODO
        }
        return switch.get(filename, None)

    def post(self, request):
        """Populates the database with the hardcoded data from the filenames in `request.body`."""
        body = json.loads(request.body)
        filenames = body.get("filenames")
        if filenames is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        new_entries = 0
        for filename in filenames:
            controller = self._filename_switch(filename)
            if controller:
                new_entries += self._parse_and_create(filename, controller)
            else:
                return failure_response(
                    f"Invalid filename {filename}", status.HTTP_406_NOT_ACCEPTABLE
                )

        if new_entries > 0:
            return success_response(
                f"Successfully created {new_entries} new entries",
                status.HTTP_201_CREATED,
            )
        else:
            return success_response("No new changes", status.HTTP_200_OK)


class CountdownDummyView(generics.GenericAPIView):
    def post(self, request):
        body = json.loads(request.body)
        seconds = body.get("seconds")
        if seconds:
            start_countdown.delay(seconds)
            return success_response(f"Countdown started for {seconds} seconds")
        return failure_response(
            "POST body is misformatted", status.HTTP_400_BAD_REQUEST
        )

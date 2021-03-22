import json

from api.utils import failure_response
from api.utils import success_response
from interest.controllers.create_interest_controller import CreateInterestController
from rest_framework import generics
from rest_framework import status as s

from . import settings as api_settings


class PopulateView(generics.GenericAPIView):
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def _parse_and_create(self, filename, controller):
        """Parses `filename` and feeds each processed line to `controller`
        to be created into a new entry if not already in the database.
        Returns the number of newly created data entries."""
        newEntries = 0
        with open(f"{api_settings.ASSETS_LOCATION}{filename}") as file:
            for line in file:
                line = line.strip().split(api_settings.ASSETS_SPLITTER)
                newEntries += 1 if controller(data=line).process() else 0
        return newEntries

    def _filename_switch(self, filename):
        """ Returns the appropriate controller class for `filename`"""
        switch = {
            "PearGroups.txt": None,  # TODO
            "PearInterests.txt": CreateInterestController,
            "PearLocations.txt": None,  # TODO
        }
        return switch.get(filename, None)

    def post(self, request):
        """ Populates the database with the hardcoded data from the filenames in `request.body` """
        try:
            body = json.loads(request.body)
            filenames = body.get("filenames")
            assert filenames
        except:
            return failure_response("POST body is misformatted", s.HTTP_400_BAD_REQUEST)

        newEntries = 0
        for filename in filenames:
            controller = self._filename_switch(filename)
            if controller:
                newEntries += self._parse_and_create(filename, controller)
            else:
                return failure_response(
                    f"Invalid filename {filename}", s.HTTP_406_NOT_ACCEPTABLE
                )

        if newEntries > 0:
            return success_response(
                f"Successfully created {newEntries} new entries", s.HTTP_201_CREATED
            )
        else:
            return success_response("No new changes", s.HTTP_200_OK)

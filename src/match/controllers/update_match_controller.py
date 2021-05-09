import datetime
import json

from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from match import match_status
from match.models import Match
from rest_framework import status


class UpdateMatchController:
    def __init__(self, match_id, user, data, serializer):
        self._match_id = match_id
        self._user = user
        self._data = data
        self._serializer = serializer

    def process(self):
        # First, find the match and any fields to be updated
        self._match = Match.objects.filter(id=self._match_id)
        if not self._match:
            return failure_response("Match does not exist.")
        self._match = self._match[0]
        proposed_meeting_times = self._data.get("proposed_meeting_times")
        proposed_locations = self._data.get("proposed_locations")
        meeting_location = self._data.get("meeting_location")
        meeting_time = self._data.get("meeting_time")

        # Next, modify the attributes that may have changed
        error_responses = []
        self._modify_attribute("proposed_meeting_times", proposed_meeting_times)
        if meeting_time is not None:
            self._update_meeting_time(meeting_time)
        if proposed_locations is not None:
            error_responses.append(self._update_proposed_locations(proposed_locations))
        if meeting_location is not None:
            error_responses.append(self._update_meeting_location(meeting_location))

        # Based on what changed, update the match status
        error_responses.append(
            self._update_match_status(
                proposed_meeting_times,
                proposed_locations,
                meeting_location,
                meeting_time,
            )
        )

        # If we had any errors, return those errors before saving
        for error in error_responses:
            if error is not None:
                return error

        self._match.save()
        return success_response()

    def _modify_attribute(self, attr_name, attr_value):
        """Modify an attribute if it isn't None and has been changed."""
        if attr_value is not None and attr_value != getattr(self._match, attr_name):
            setattr(self._match, attr_name, attr_value)

    def _update_proposed_locations(self, body_proposed_locations):
        """Update the proposed locations."""
        for new_location_id in body_proposed_locations:
            new_location = Location.objects.filter(id=new_location_id)
            if not new_location:
                return failure_response(
                    f"Location with id {new_location_id} does not exist."
                )
            if new_location[0] not in self._match.proposed_locations.all():
                self._match.proposed_locations.add(new_location[0])
        for existing_location in self._match.proposed_locations.all():
            if existing_location.id not in body_proposed_locations:
                self._match.proposed_locations.remove(existing_location)

    def _update_meeting_location(self, body_meeting_location_id):
        """Update the meeting location."""
        new_meeting_location = Location.objects.filter(id=body_meeting_location_id)
        if not new_meeting_location:
            return failure_response(
                f"Location with id {body_meeting_location_id} does not exist."
            )
        self._modify_attribute("meeting_location", new_meeting_location[0])

    def _update_meeting_time(self, times):
        """Given a list with one time, generate a timestamp.
        Example: ["", "", "9.5", "", "", "", ""] turns into
        '2021-05-11 09:30:00' i.e. the Tuesday after now() at 9:30 am
        """
        # simple_meeting is [weekday, time] from times param
        simple_meeting = [0, 0]
        for index in range(len(times)):
            if times[index] != "":
                simple_meeting = index, float(times[index])
        now = datetime.datetime.now()
        hour, minute = divmod(simple_meeting[1], 1)
        minute *= 60
        days = (6 - now.weekday() + simple_meeting[0]) % 7
        meeting_time = (now + datetime.timedelta(days=days)).replace(
            hour=int(hour), minute=int(minute), second=0, microsecond=0
        )
        self._match.meeting_time = meeting_time

    def _update_match_status(
        self, proposed_meeting_times, proposed_locations, meeting_location, meeting_time
    ):
        """Update status based on match field changes."""
        if proposed_meeting_times is not None and proposed_locations is not None:
            # In case match is already proposed
            if self._match.status == match_status.PROPOSED:
                return failure_response(
                    "Match has already been proposed", status.HTTP_400_BAD_REQUEST
                )
            self._match.status = match_status.PROPOSED
            self._match.proposer_id = self._user.id
            self._match.accepted_ids = [self._user.id]
        elif meeting_location is not None and meeting_time is not None:
            # In case match is already active
            if self._match.status == match_status.ACTIVE:
                return failure_response(
                    "Match has already been accepted", status.HTTP_400_BAD_REQUEST
                )
            self._match.status = match_status.ACTIVE
            # use json.loads to convert a string of a list to an actual list
            accepted_ids = json.loads(self._match.accepted_ids)
            if self._user.id not in accepted_ids:
                accepted_ids.append(self._user.id)
                self._match.accepted_ids = accepted_ids
            self._match.proposed_meeting_times = None
            self._match.proposed_locations.set([])

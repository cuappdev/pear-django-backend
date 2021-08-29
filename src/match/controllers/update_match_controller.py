import datetime
import json

from api.utils import failure_response
from api.utils import modify_attribute
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
        meeting_location_id = self._data.get("meeting_location")
        meeting_time = self._data.get("meeting_time")

        # Next, modify the attributes that may have changed:
        # Proposed Meeting Times
        modify_attribute("proposed_meeting_times", json.dumps(proposed_meeting_times))
        # Meeting Time
        if meeting_time is not None:
            self._update_meeting_time(meeting_time)
        # Proposed Locations
        if proposed_locations is not None:
            new_locations = []
            for loc_id in proposed_locations:
                new_location = Location.objects.filter(id=loc_id)
                if not new_location:
                    return failure_response(f"Location id {loc_id} does not exist.")
                new_locations.append(new_location[0])
            self._match.proposed_locations.set(new_locations)
        # Meeting Location
        if meeting_location_id is not None:
            new_meeting_location = Location.objects.filter(id=meeting_location_id)
            if not new_meeting_location:
                return failure_response(
                    f"Location with id {meeting_location_id} does not exist."
                )
            modify_attribute("meeting_location", new_meeting_location[0])

        # Based on what changed, check for status conflicts
        if proposed_meeting_times is not None and proposed_locations is not None:
            # In case match is already proposed
            if self._match.status == match_status.PROPOSED:
                return failure_response(
                    "Match has already been proposed", status.HTTP_400_BAD_REQUEST
                )
        elif meeting_location_id is not None and meeting_time is not None:
            # In case match is already active
            if self._match.status == match_status.ACTIVE:
                return failure_response(
                    "Match has already been accepted", status.HTTP_400_BAD_REQUEST
                )

        # Finally, update the match status
        self._update_match_status(
            proposed_meeting_times,
            proposed_locations,
            meeting_location_id,
            meeting_time,
        )

        self._match.save()
        return success_response()

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
            self._match.status = match_status.PROPOSED
            self._match.proposer_id = self._user.id
            self._match.accepted_ids = json.dumps([self._user.id])
        elif meeting_location is not None and meeting_time is not None:
            self._match.status = match_status.ACTIVE
            # use json.loads to convert a string of a list to an actual list
            accepted_ids = json.loads(self._match.accepted_ids)
            if self._user.id not in accepted_ids:
                accepted_ids.append(self._user.id)
                self._match.accepted_ids = json.dumps(accepted_ids)
            self._match.proposed_meeting_times = None
            self._match.proposed_locations.set([])

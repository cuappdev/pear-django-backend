import json

from api.utils import failure_response
from api.utils import success_response
from django.core.exceptions import ValidationError
from location.models import Location
from match import match_status
from match.models import Match
from match.validators import validate_int_list
from match.validators import validate_times_list
from rest_framework import status


class UpdateMatchController:
    def __init__(self, match_id, request, data, serializer):
        self._match_id = match_id
        self._request = request
        self._serializer = serializer
        self._data = data

    def process(self):
        """Update match fields that have changed."""
        self._match = Match.objects.filter(id=self._match_id)
        if not self._match:
            return failure_response("Match does not exist.")
        self._match = self._match[0]
        status = self._data.get("status")
        accepted_ids = self._data.get("accepted_ids")
        proposed_meeting_times = self._data.get("proposed_meeting_times")
        proposed_locations = self._data.get("proposed_locations")
        meeting_location = self._data.get("meeting_location")
        meeting_time = self._data.get("meeting_time")
        output_messages = []
        output_messages.append(
            self._validate_acceptors_and_times(accepted_ids, proposed_meeting_times)
        )
        output_messages.append(self._validate_status(status))
        self._update_proposer_and_acceptors(status)
        self._modify_attribute("status", status)
        self._modify_attribute("accepted_ids", accepted_ids)
        self._modify_attribute("proposed_meeting_times", proposed_meeting_times)
        self._modify_attribute("meeting_time", meeting_time)
        if proposed_locations is not None:
            output_messages.append(self._update_proposed_locations(proposed_locations))
        if meeting_location is not None:
            output_messages.append(self._update_meeting_location(meeting_location))
        self._validate_match_status()
        for error in output_messages:
            if error is not None:
                return error
        self._match.save()
        return success_response()

    def _modify_attribute(self, attr_name, attr_value):
        """Modify an attribute if it isn't None and has been changed."""
        if attr_value is not None and attr_value != getattr(self._match, attr_name):
            setattr(self._match, attr_name, attr_value)

    def _validate_acceptors_and_times(self, body_accepted_ids, body_proposed_times):
        """Ensure that these fields are proper lists."""
        try:
            if body_accepted_ids is not None:
                validate_int_list(body_accepted_ids)
            if body_proposed_times is not None:
                validate_times_list(body_proposed_times)
        except ValidationError as e:
            return failure_response(e, status.HTTP_400_BAD_REQUEST)

    def _validate_status(self, status):
        """Ensure that status is a valid match status."""
        possible_statuses = [
            match_status.CREATED,
            match_status.PROPOSED,
            match_status.ACTIVE,
            match_status.INACTIVE,
            match_status.CANCELED,
        ]
        if status not in possible_statuses:
            return failure_response(f"Status '{status}' is not a valid match status.")

    def _update_proposer_and_acceptors(self, status):
        """Updates the proposer_id and accepted_ids if status changes."""
        if status == match_status.PROPOSED:
            self._match.proposer_id = self._request.user.id
            self._match.accepted_ids = [self._request.user.id]
        if status == match_status.ACTIVE:
            current_accepted_ids = json.loads(self._match.accepted_ids)
            if self._request.user.id not in current_accepted_ids:
                current_accepted_ids.append(self._request.user.id)
                self._match.accepted_ids = current_accepted_ids

    def _update_proposed_locations(self, body_proposed_locations):
        """Update the proposed locations."""
        for new_location_id in body_proposed_locations:
            try:
                new_location_id = int(new_location_id)
            except (ValueError, TypeError):
                return failure_response(
                    f"Location {new_location_id} does not exist",
                    status.HTTP_400_BAD_REQUEST,
                )
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

    def _validate_match_status(self):
        """Ensure that certain fields are set to None for status changes."""
        if self._match.status == match_status.CREATED:
            self._match.proposer_id = None
            self._match.accepted_ids = None
            self._match.proposed_meeting_times = None
            self._match.proposed_locations.set([])
            self._match.meeting_location = None
            self._match.meeting_time = None
        elif self._match.status == match_status.PROPOSED:
            self._match.meeting_location = None
            self._match.meeting_time = None
        elif self._match.status == match_status.ACTIVE:
            self._match.proposed_meeting_times = None
            self._match.proposed_locations.set([])
        elif self._match.status == match_status.INACTIVE:
            self._match.proposed_meeting_times = None
            self._match.proposed_locations.set([])
        elif self._match.status == match_status.CANCELED:
            self._match.proposed_meeting_times = None
            self._match.proposed_locations.set([])
            self._match.meeting_location = None
            self._match.meeting_time = None

from api.utils import failure_response
from api.utils import success_response
from location.models import Location
from match.models import Match


class UpdateMatchController:
    def __init__(self, match_id, request, data, serializer):
        self._match = Match.objects.filter(id=match_id)[0]
        self._request = request
        self._serializer = serializer
        self._data = data

    def process(self):
        """Update match fields that have changed."""
        proposer_id = self._data.get("proposer_id")
        accepted_ids = self._data.get("accepted_ids")
        proposed_meeting_times = self._data.get("proposed_meeting_times")
        proposed_locations = self._data.get("proposed_locations")
        meeting_location = self._data.get("meeting_location")
        meeting_time = self._data.get("meeting_time")

        self._modify_attribute("proposer_id", proposer_id)
        self._modify_attribute("accepted_ids", accepted_ids)
        self._modify_attribute("proposed_meeting_times", proposed_meeting_times)
        if proposed_locations is not None:
            for new_location_id in proposed_locations:
                new_location = Location.objects.filter(id=new_location_id)
                if not new_location:
                    return failure_response(
                        f"Location with id {new_location_id} does not exist."
                    )
                if new_location[0] not in self._match.proposed_locations.all():
                    self._match.proposed_locations.add(new_location[0])
            for existing_location in self._match.proposed_locations.all():
                if existing_location.id not in proposed_locations:
                    self._match.proposed_locations.remove(existing_location)
        if meeting_location is not None:
            new_meeting_location = Location.objects.filter(id=meeting_location)
            if not new_meeting_location:
                return failure_response(
                    f"Location with id {meeting_location} does not exist."
                )
            self._modify_attribute("meeting_location", new_meeting_location[0])
        self._modify_attribute("meeting_time", meeting_time)
        self._match.save()
        return success_response()

    def _modify_attribute(self, attr_name, attr_value):
        """Modify an attribute if it isn't None and has been changed."""
        if attr_value is not None and attr_value != getattr(self._match, attr_name):
            setattr(self._match, attr_name, attr_value)

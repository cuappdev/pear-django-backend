import json

from location.serializers import LocationSerializer
from match.models import Match
from person.simple_serializers import SimpleUserSerializer
from rest_framework import serializers


class MatchSerializer(serializers.ModelSerializer):
    matched_user = serializers.SerializerMethodField("get_matched_user")
    accepted_ids = serializers.SerializerMethodField("get_accepted_ids")
    proposed_meeting_times = serializers.SerializerMethodField(
        "get_proposed_meeting_times"
    )
    proposed_locations = serializers.SerializerMethodField("get_proposed_locations")
    meeting_location = serializers.SerializerMethodField("get_meeting_location")

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def get_matched_user(self, match):
        if self.request_user == match.user_1:
            return SimpleUserSerializer(match.user_2).data
        elif self.request_user == match.user_2:
            return SimpleUserSerializer(match.user_1).data

    def get_accepted_ids(self, match):
        if match.accepted_ids is None:
            return None
        accepted_ids = json.loads(match.accepted_ids)
        return accepted_ids or None

    def get_proposed_meeting_times(self, match):
        if match.proposed_meeting_times is None:
            return None
        # We have to replace all single quotes with double quotes for JSON
        proposed_meeting_times = json.loads(
            match.proposed_meeting_times.replace("'", '"')
        )
        if proposed_meeting_times == []:
            return None
        return proposed_meeting_times

    def get_proposed_locations(self, match):
        proposed_locations = []
        for location in match.proposed_locations.all():
            proposed_locations.append(LocationSerializer(location).data)
        if proposed_locations == []:
            return None
        return proposed_locations

    def get_meeting_location(self, match):
        meeting_location = LocationSerializer(match.meeting_location).data
        if meeting_location == {}:
            return None
        return meeting_location

    class Meta:
        model = Match
        fields = (
            "id",
            "status",
            "matched_user",
            "proposer_id",
            "accepted_ids",
            "proposed_meeting_times",
            "proposed_locations",
            "meeting_location",
            "meeting_time",
        )
        read_only_fields = fields


class BothUsersMatchSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField("get_users")
    accepted_ids = serializers.SerializerMethodField("get_accepted_ids")
    proposed_meeting_times = serializers.SerializerMethodField(
        "get_proposed_meeting_times"
    )
    proposed_locations = serializers.SerializerMethodField("get_proposed_locations")
    meeting_location = serializers.SerializerMethodField("get_meeting_location")

    def get_users(self, match):
        serializer = SimpleUserSerializer(data=[match.user_1, match.user_2], many=True)
        # because data is passed w/ multiple users, check validity before returning
        serializer.is_valid()
        return serializer.data

    def get_accepted_ids(self, match):
        if match.accepted_ids is None:
            return None
        accepted_ids = json.loads(match.accepted_ids)
        return accepted_ids or None

    def get_proposed_meeting_times(self, match):
        if match.proposed_meeting_times is None:
            return None
        proposed_meeting_times = json.loads(
            match.proposed_meeting_times.replace("'", '"')
        )
        if proposed_meeting_times == []:
            return None
        return proposed_meeting_times

    def get_proposed_locations(self, match):
        return (
            LocationSerializer(match.proposed_locations.all(), many=True).data or None
        )

    def get_meeting_location(self, match):
        meeting_location = LocationSerializer(match.meeting_location).data
        return meeting_location or None

    class Meta:
        model = Match
        fields = (
            "id",
            "status",
            "users",
            "proposer_id",
            "accepted_ids",
            "proposed_meeting_times",
            "proposed_locations",
            "meeting_location",
            "meeting_time",
        )
        read_only_fields = fields

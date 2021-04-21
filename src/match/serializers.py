from location.serializers import LocationSerializer
from match.models import Match
from person.serializers import UserSerializer
from rest_framework import serializers


class MatchSerializer(serializers.ModelSerializer):
    matched_user = serializers.SerializerMethodField("get_matched_user")
    proposed_locations = serializers.SerializerMethodField("get_proposed_locations")
    meeting_location = serializers.SerializerMethodField("get_meeting_location")

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def get_matched_user(self, match):
        if self.request_user.id == match.user_1.id:
            return UserSerializer(match.user_2).data
        elif self.request_user.id == match.user_2.id:
            return UserSerializer(match.user_1).data

    def get_proposed_locations(self, match):
        proposed_locations = []
        for location in match.proposed_locations.all():
            proposed_locations.append(LocationSerializer(location).data)
        return proposed_locations

    def get_meeting_location(self, match):
        return LocationSerializer(match.meeting_location).data

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
    class Meta:
        model = Match
        fields = (
            "id",
            "status",
            "user_1",
            "user_2",
            "proposer_id",
            "accepted_ids",
            "proposed_meeting_times",
            "proposed_locations",
            "meeting_location",
            "meeting_time",
        )

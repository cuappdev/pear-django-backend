import json

from django.contrib.auth.models import User
from django.db.models import Q
from group.serializers import GroupSerializer
from interest.serializers import InterestSerializer
from location.serializers import LocationSerializer
from match.models import Match
from match.serializers import MatchSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


class AuthenticateSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField(method_name="get_access_token")

    class Meta:
        model = User
        fields = (
            "access_token",
            User.USERNAME_FIELD,
            "first_name",
            "last_name",
        )
        read_only_fields = fields

    def get_access_token(self, instance):
        return self.context.get("access_token")


class UserSerializer(serializers.ModelSerializer):
    """Serializer with match history."""

    net_id = serializers.CharField(source="person.net_id")
    hometown = serializers.CharField(source="person.hometown")
    profile_pic_url = serializers.CharField(source="person.profile_pic_url")
    facebook_url = serializers.CharField(source="person.facebook_url")
    instagram_username = serializers.CharField(source="person.instagram_username")
    graduation_year = serializers.CharField(source="person.graduation_year")
    pronouns = serializers.CharField(source="person.pronouns")
    goals = SerializerMethodField("get_goals")
    talking_points = SerializerMethodField("get_talking_points")
    availability = SerializerMethodField("get_availability")
    locations = LocationSerializer(source="person.locations", many=True)
    interests = InterestSerializer(source="person.interests", many=True)
    groups = GroupSerializer(source="person.groups", many=True)
    has_onboarded = serializers.BooleanField(source="person.has_onboarded")
    matches = serializers.SerializerMethodField("get_match_history")

    def get_goals(self, user):
        if user.person.goals is None:
            return None
        print(user.person.goals)
        goals = json.loads(user.person.goals.replace("'", '"'))
        return goals or None

    def get_talking_points(self, user):
        if user.person.talking_points is None:
            return None
        talking_points = json.loads(user.person.talking_points.replace("'", '"'))
        return talking_points or None

    def get_availability(self, user):
        if user.person.availability is None:
            return None
        availability = json.loads(user.person.availability.replace("'", '"'))
        return availability or None

    def get_match_history(self, user):
        matches = Match.objects.filter(Q(user_1=user) | Q(user_2=user)).order_by(
            "-created_date"
        )
        return MatchSerializer(matches, user=user, many=True).data

    class Meta:
        model = User
        fields = (
            "id",
            "net_id",
            "first_name",
            "last_name",
            "hometown",
            "profile_pic_url",
            "facebook_url",
            "instagram_username",
            "graduation_year",
            "pronouns",
            "goals",
            "talking_points",
            "availability",
            "locations",
            "interests",
            "groups",
            "has_onboarded",
            "matches",
        )
        read_only_fields = fields


class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializer for all users view."""

    net_id = serializers.CharField(source="person.net_id")
    profile_pic_url = serializers.CharField(source="person.profile_pic_url")
    interests = InterestSerializer(source="person.interests", many=True)
    groups = GroupSerializer(source="person.groups", many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "net_id",
            "first_name",
            "last_name",
            "profile_pic_url",
            "interests",
            "groups",
        )
        read_only_fields = fields

import json

from django.contrib.auth.models import User
from django.db.models import Q
from group.serializers import GroupSerializer
from interest.serializers import InterestSerializer
from location.serializers import LocationSerializer
from major.serializers import MajorSerializer
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
    majors = MajorSerializer(source="person.majors", many=True)
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
    prompts = SerializerMethodField("get_prompts")
    has_onboarded = serializers.BooleanField(source="person.has_onboarded")
    pending_feedback = serializers.BooleanField(source="person.pending_feedback")
    current_match = serializers.SerializerMethodField("get_current_match")

    def get_goals(self, user):
        if user.person.goals is None:
            return []
        goals = json.loads(user.person.goals.replace("'", '"'))
        return goals

    def get_talking_points(self, user):
        if user.person.talking_points is None:
            return []
        talking_points = json.loads(user.person.talking_points.replace("'", '"'))
        return talking_points

    def get_availability(self, user):
        if user.person.availability is None:
            return []
        availability = json.loads(user.person.availability.replace("'", '"'))
        return availability

    def get_current_match(self, user):
        matches = Match.objects.filter(Q(user_1=user) | Q(user_2=user)).order_by(
            "-created_date"
        )
        if len(matches) == 0:
            return None
        return MatchSerializer(matches[0], user=user).data

    def get_prompts(self, user):
        prompt_questions = user.person.prompt_questions.all()
        prompt_answers = user.person.prompt_answers
        if prompt_answers is None:
            return []
        # We have to replace all single quotes with double quotes for JSON
        prompt_answers = json.loads(prompt_answers.replace("'", '"'))
        prompts = []
        for question_index in range(len(prompt_questions)):
            prompts.append(
                {
                    "question_id": prompt_questions[question_index].id,
                    "question_name": prompt_questions[question_index].question_name,
                    "label_users_see": prompt_questions[question_index].label_users_see,
                    "answer": prompt_answers[question_index],
                }
            )
        return prompts

    class Meta:
        model = User
        fields = (
            "id",
            "net_id",
            "first_name",
            "last_name",
            "majors",
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
            "prompts",
            "has_onboarded",
            "pending_feedback",
            "current_match",
        )
        read_only_fields = fields


class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializer for all users view."""

    net_id = serializers.CharField(source="person.net_id")
    profile_pic_url = serializers.CharField(source="person.profile_pic_url")
    majors = MajorSerializer(source="person.majors", many=True)
    hometown = serializers.CharField(source="person.hometown")
    graduation_year = serializers.CharField(source="person.graduation_year")
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
            "majors",
            "hometown",
            "graduation_year",
            "interests",
            "groups",
        )
        read_only_fields = fields


class AllMatchesSerializer(serializers.ModelSerializer):
    """Serializer to get all of one user's matches."""

    matches = serializers.SerializerMethodField("get_all_matches")

    def get_all_matches(self, user):
        matches = Match.objects.filter(Q(user_1=user) | Q(user_2=user)).order_by(
            "-created_date"
        )
        return MatchSerializer(matches, user=user, many=True).data

    class Meta:
        model = User
        fields = ("matches",)

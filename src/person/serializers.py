import json

from django.contrib.auth.models import User
from django.db.models import Q
from group.serializers import GroupSerializer
from interest.serializers import InterestSerializer
from location.serializers import LocationSerializer
from major.serializers import MajorSerializer
from match.models import Match
from match.serializers import MatchSerializer
from purpose.serializers import PurposeSerializer
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
    purposes = PurposeSerializer(source="person.purposes", many=True)
    availability = SerializerMethodField("get_availability")
    locations = LocationSerializer(source="person.locations", many=True)
    interests = InterestSerializer(source="person.interests", many=True)
    groups = GroupSerializer(source="person.groups", many=True)
    prompts = SerializerMethodField("get_prompts")
    has_onboarded = serializers.BooleanField(source="person.has_onboarded")
    pending_feedback = serializers.BooleanField(source="person.pending_feedback")
    current_match = serializers.SerializerMethodField("get_current_match")
    deleted = serializers.BooleanField(source="person.soft_deleted")
    is_paused = serializers.BooleanField(source="person.is_paused")
    pause_expiration = serializers.DateTimeField(source="person.pause_expiration")

    def get_availability(self, user):
        if user.person.availability is None:
            return []
        availability = json.loads(user.person.availability)
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
        prompt_answers = json.loads(prompt_answers)
        prompts = []
        for question_index in range(len(prompt_questions)):
            prompts.append(
                {
                    "id": prompt_questions[question_index].id,
                    "question_name": prompt_questions[question_index].question_name,
                    "question_placeholder": prompt_questions[
                        question_index
                    ].question_placeholder,
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
            "purposes",
            "availability",
            "locations",
            "interests",
            "groups",
            "prompts",
            "has_onboarded",
            "deleted",
            "pending_feedback",
            "current_match",
            "is_paused",
            "pause_expiration",
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

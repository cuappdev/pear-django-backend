import json

from django.contrib.auth.models import User
from group.serializers import GroupSerializer
from interest.serializers import InterestSerializer
from major.serializers import MajorSerializer
from rest_framework import serializers


class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializer for all users view."""

    net_id = serializers.CharField(source="person.net_id")
    profile_pic_url = serializers.CharField(source="person.profile_pic_url")
    majors = MajorSerializer(source="person.majors", many=True)
    hometown = serializers.CharField(source="person.hometown")
    graduation_year = serializers.CharField(source="person.graduation_year")
    pronouns = serializers.CharField(source="person.pronouns")
    interests = InterestSerializer(source="person.interests", many=True)
    groups = GroupSerializer(source="person.groups", many=True)
    prompts = serializers.SerializerMethodField("get_prompts")
    pending_feedback = serializers.BooleanField(source="person.pending_feedback")
    blocked = serializers.SerializerMethodField("get_blocked")

    def get_blocked(self, user):
        request_user = self.context.get("request_user")
        if request_user is not None:
            return user.id in request_user.person.blocked_users.values_list(
                "id", flat=True
            )
        return None

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
            "profile_pic_url",
            "majors",
            "hometown",
            "graduation_year",
            "pronouns",
            "interests",
            "groups",
            "prompts",
            "pending_feedback",
            "blocked",
        )
        read_only_fields = fields

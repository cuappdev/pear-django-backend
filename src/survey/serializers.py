import json

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from survey import constants
from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):

    did_not_meet_reasons = SerializerMethodField("get_did_not_meet_reasons")

    def get_did_not_meet_reasons(self, survey):
        if survey.did_not_meet_reasons is None:
            return []
        return map(
            lambda x: constants.short_to_long(x),
            json.loads(survey.did_not_meet_reasons),
        )

    class Meta:
        model = Survey
        fields = (
            "id",
            "did_meet",
            "did_meet_reason",
            "rating",
            "submitting_person",
            "completed_match",
            "did_not_meet_reasons",
        )
        read_only_fields = fields

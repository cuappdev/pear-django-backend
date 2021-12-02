from rest_framework import serializers
from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ("id", "did_meet", "explanation", "rating")
        read_only_fields = fields

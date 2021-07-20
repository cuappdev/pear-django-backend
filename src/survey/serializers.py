from rest_framework import serializers
from survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ("id", "explanation", "rating")
        read_only_fields = fields

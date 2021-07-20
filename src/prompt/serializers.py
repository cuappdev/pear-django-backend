from prompt.models import Prompt
from rest_framework import serializers


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ("id", "question_name", "label_users_see")
        read_only_fields = fields

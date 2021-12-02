from purpose.models import Purpose
from rest_framework import serializers


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = ("id", "name")
        read_only_fields = fields

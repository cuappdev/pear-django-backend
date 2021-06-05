from major.models import Major
from rest_framework import serializers


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ("id", "name")
        read_only_fields = fields

from group.models import Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")
        read_only_fields = fields

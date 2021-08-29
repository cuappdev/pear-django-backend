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
        )
        read_only_fields = fields

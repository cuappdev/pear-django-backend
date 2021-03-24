from django.contrib.auth.models import User
from rest_framework import serializers


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
    net_id = serializers.CharField(source="person.net_id")
    hometown = serializers.CharField(source="person.hometown")
    profile_pic_url = serializers.CharField(source="person.profile_pic_url")
    facebook_url = serializers.CharField(source="person.facebook_url")
    instagram_username = serializers.CharField(source="person.instagram_username")
    graduation_year = serializers.CharField(source="person.graduation_year")
    pronouns = serializers.CharField(source="person.pronouns")

    class Meta:
        model = User
        fields = (
            "id",
            "net_id",
            "first_name",
            "last_name",
            "hometown",
            "profile_pic_url",
            "facebook_url",
            "instagram_username",
            "graduation_year",
            "pronouns",
        )
        read_only_fields = fields

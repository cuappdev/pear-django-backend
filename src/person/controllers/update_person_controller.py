from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
import requests
from rest_framework import status


class UpdatePersonController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer
        self._user = self._request.user
        self._person = self._user.person

    def process(self):
        """Update person fields that have changed."""
        net_id = self._data.get("net_id")
        first_name = self._data.get("first_name")
        last_name = self._data.get("last_name")
        hometown = self._data.get("hometown")
        profile_pic_base64 = self._data.get("profile_pic_base64")
        profile_pic_url = self._data.get("profile_pic_url")
        facebook_url = self._data.get("facebook_url")
        instagram_username = self._data.get("instagram_username")
        graduation_year = self._data.get("graduation_year")
        pronouns = self._data.get("pronouns")

        if profile_pic_base64 is not None:
            upload_response = self._upload_profile_pic(profile_pic_base64)
            if upload_response:
                self._person.profile_pic_url = self._get_value(
                    upload_response.json().get("data"), self._person.profile_pic_url
                )
            else:
                return failure_response(
                    f"Unable to upload image to AppDev Upload service:{upload_response.status_code}",
                    status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        self._person.net_id = self._get_value(net_id, self._person.net_id)
        self._user.first_name = self._get_value(first_name, self._user.first_name)
        self._user.last_name = self._get_value(last_name, self._user.last_name)
        self._person.hometown = self._get_value(hometown, self._person.hometown)
        self._person.profile_pic_url = self._get_value(
            profile_pic_url, self._person.profile_pic_url
        )
        self._person.facebook_url = self._get_value(
            facebook_url, self._person.facebook_url
        )
        self._person.instagram_username = self._get_value(
            instagram_username, self._person.instagram_username
        )
        self._person.graduation_year = self._get_value(
            graduation_year, self._person.graduation_year
        )
        self._person.pronouns = self._get_value(pronouns, self._person.pronouns)
        self._user.save()
        self._person.save()
        return success_response(self._serializer(self._user).data)

    def _get_value(self, v, default):
        """Get value, or get default if value is None."""
        if v is None:
            return default
        else:
            return v

    def _upload_profile_pic(self, profile_pic_base64):
        """Uploads image to AppDev Upload service, and modifies Person's profile_pic_url if successful. Returns the HTTP Response."""
        request_body = {"bucket": "pear", "image": profile_pic_base64}
        response = requests.post(api_settings.UPLOAD_URL, json=request_body)
        return response

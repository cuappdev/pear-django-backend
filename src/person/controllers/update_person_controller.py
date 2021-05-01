from api.utils import modify_attribute
from api.utils import success_response
from rest_framework import status

from ..tasks import upload_profile_pic


class UpdatePersonController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer
        self._user = self._request.user
        self._person = self._user.person

    def process(self):
        net_id = self._data.get("net_id")
        first_name = self._data.get("first_name")
        last_name = self._data.get("last_name")
        hometown = self._data.get("hometown")
        profile_pic_base64 = self._data.get("profile_pic_base64")
        facebook_url = self._data.get("facebook_url")
        instagram_username = self._data.get("instagram_username")
        graduation_year = self._data.get("graduation_year")
        pronouns = self._data.get("pronouns")

        if profile_pic_base64 is not None:
            upload_profile_pic.delay(self._user.id, profile_pic_base64)

        modify_attribute(self._person, "net_id", net_id)
        modify_attribute(self._user, "first_name", first_name)
        modify_attribute(self._user, "last_name", last_name)
        modify_attribute(self._person, "hometown", hometown)
        modify_attribute(self._person, "facebook_url", facebook_url)
        modify_attribute(self._person, "instagram_username", instagram_username)
        modify_attribute(self._person, "graduation_year", graduation_year)
        modify_attribute(self._person, "pronouns", pronouns)
        self._user.save()
        self._person.save()
        return success_response(status=status.HTTP_200_OK)

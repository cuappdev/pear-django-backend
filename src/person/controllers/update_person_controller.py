from api.utils import success_response


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
        profile_pic_url = self._data.get("profile_pic_url")
        facebook_url = self._data.get("facebook_url")
        instagram_username = self._data.get("instagram_username")
        graduation_year = self._data.get("graduation_year")
        pronouns = self._data.get("pronouns")

        if net_id is not None and self._person.net_id != net_id:
            self._person.net_id = net_id
        if first_name is not None and self._user.first_name != first_name:
            self._user.first_name = first_name
        if last_name is not None and self._user.last_name != last_name:
            self._user.last_name = last_name
        if hometown is not None and self._person.hometown != hometown:
            self._person.hometown = hometown
        if (
            profile_pic_url is not None
            and self._person.profile_pic_url != profile_pic_url
        ):
            self._person.profile_pic_url = profile_pic_url
        if facebook_url is not None and self._person.facebook_url != facebook_url:
            self._person.facebook_url = facebook_url
        if (
            instagram_username is not None
            and self._person.instagram_username != instagram_username
        ):
            self._person.instagram_username = instagram_username
        if (
            graduation_year is not None
            and self._person.graduation_year != graduation_year
        ):
            self._person.graduation_year = graduation_year
        if pronouns is not None and self._person.pronouns != pronouns:
            self._person.pronouns = pronouns

        self._user.save()
        self._person.save()
        return success_response(self._serializer(self._user).data)

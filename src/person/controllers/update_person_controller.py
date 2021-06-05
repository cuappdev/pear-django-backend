from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from group.models import Group
from interest.models import Interest
from location.models import Location
from rest_framework import status

from ..tasks import upload_profile_pic


class UpdatePersonController:
    def __init__(self, user, data, serializer):
        self._data = data
        self._serializer = serializer
        self._user = user
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

        goals = self._data.get("goals")
        talking_points = self._data.get("talking_points")

        availability = self._data.get("availability")
        locations = self._data.get("locations")
        groups = self._data.get("groups")
        interests = self._data.get("interests")

        has_onboarded = self._data.get("has_onboarded")

        if profile_pic_base64 is not None:
            upload_profile_pic.delay(self._user.id, profile_pic_base64)

        if locations is not None:
            new_locations = []
            for loc_id in locations:
                new_location = Location.objects.filter(id=loc_id)
                if not new_location:
                    return failure_response(f"Location id {loc_id} does not exist.")
                new_locations.append(new_location[0])
            self._person.locations.set(new_locations)

        if groups is not None:
            new_groups = []
            for group_id in groups:
                new_group = Group.objects.filter(id=group_id)
                if not new_group:
                    return failure_response(f"Group id {group_id} does not exist.")
                new_groups.append(new_group[0])
            self._person.groups.set(new_groups)

        if interests is not None:
            new_interests = []
            for interest_id in interests:
                new_interest = Interest.objects.filter(id=interest_id)
                if not new_interest:
                    return failure_response(
                        f"Interest id {interest_id} does not exist."
                    )
                new_interests.append(new_interest[0])
            self._person.interests.set(new_interests)

        modify_attribute(self._person, "net_id", net_id)
        modify_attribute(self._user, "first_name", first_name)
        modify_attribute(self._user, "last_name", last_name)
        modify_attribute(self._person, "hometown", hometown)
        modify_attribute(self._person, "facebook_url", facebook_url)
        modify_attribute(self._person, "instagram_username", instagram_username)
        modify_attribute(self._person, "graduation_year", graduation_year)
        modify_attribute(self._person, "pronouns", pronouns)
        modify_attribute(self._person, "goals", goals)
        modify_attribute(self._person, "talking_points", talking_points)
        modify_attribute(self._person, "has_onboarded", has_onboarded)
        modify_attribute(self._person, "availability", availability)
        self._user.save()
        self._person.save()
        return success_response(status=status.HTTP_200_OK)

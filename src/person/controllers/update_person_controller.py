import json

from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from group.models import Group
from interest.models import Interest
from location.models import Location
from major.models import Major
from prompt.models import Prompt
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
        major_ids = self._data.get("majors")
        hometown = self._data.get("hometown")
        profile_pic_base64 = self._data.get("profile_pic_base64")
        facebook_url = self._data.get("facebook_url")
        instagram_username = self._data.get("instagram_username")
        graduation_year = self._data.get("graduation_year")
        pronouns = self._data.get("pronouns")
        # goals = self._data.get("goals")
        talking_points = self._data.get("talking_points")
        availability = self._data.get("availability")
        location_ids = self._data.get("locations")
        group_ids = self._data.get("groups")
        prompts = self._data.get("prompts")
        interest_ids = self._data.get("interests")
        has_onboarded = self._data.get("has_onboarded")
        pending_feedback = self._data.get("pending_feedback")

        if major_ids is not None:
            new_majors = []
            for id in major_ids:
                new_major = Major.objects.filter(id=id)
                if not new_major:
                    return failure_response(f"Major id {id} does not exist.")
                new_majors.append(new_major[0])
            self._person.majors.set(new_majors)

        if profile_pic_base64 is not None:
            upload_profile_pic.delay(self._user.id, profile_pic_base64)

        if location_ids is not None:
            new_locations = []
            for loc_id in location_ids:
                new_location = Location.objects.filter(id=loc_id)
                if not new_location:
                    return failure_response(f"Location id {loc_id} does not exist.")
                new_locations.append(new_location[0])
            self._person.locations.set(new_locations)

        if group_ids is not None:
            new_groups = []
            for group_id in group_ids:
                new_group = Group.objects.filter(id=group_id)
                if not new_group:
                    return failure_response(f"Group id {group_id} does not exist.")
                new_groups.append(new_group[0])
            self._person.groups.set(new_groups)

        if interest_ids is not None:
            new_interests = []
            for interest_id in interest_ids:
                new_interest = Interest.objects.filter(id=interest_id)
                if not new_interest:
                    return failure_response(
                        f"Interest id {interest_id} does not exist."
                    )
                new_interests.append(new_interest[0])
            self._person.interests.set(new_interests)

        if prompts is not None:
            prompt_questions = []
            prompt_answers = []
            for prompt in prompts:
                prompt_id = prompt.get("id")
                prompt_question = Prompt.objects.filter(id=prompt_id)
                if not prompt_question:
                    return failure_response(f"Prompt id {prompt_id} does not exist.")
                prompt_questions.append(prompt_question[0])
                prompt_answers.append(prompt.get("answer"))
            self._person.prompt_questions.set(prompt_questions)
            modify_attribute(self._person, "prompt_answers", json.dumps(prompt_answers))

        modify_attribute(self._person, "net_id", net_id)
        modify_attribute(self._user, "first_name", first_name)
        modify_attribute(self._user, "last_name", last_name)
        modify_attribute(self._person, "hometown", hometown)
        modify_attribute(self._person, "facebook_url", facebook_url)
        modify_attribute(self._person, "instagram_username", instagram_username)
        modify_attribute(self._person, "graduation_year", graduation_year)
        modify_attribute(self._person, "pronouns", pronouns)
        # modify_attribute(self._person, "goals", json.dumps(goals))
        modify_attribute(self._person, "talking_points", json.dumps(talking_points))
        modify_attribute(self._person, "has_onboarded", has_onboarded)
        modify_attribute(self._person, "pending_feedback", pending_feedback)
        modify_attribute(self._person, "availability", json.dumps(availability))
        self._user.save()
        self._person.save()
        return success_response(status=status.HTTP_200_OK)

from datetime import datetime
from datetime import timedelta
import json

from api.utils import failure_response
from api.utils import modify_attribute
from api.utils import success_response
from api.utils import update_many_to_many_set
from group.models import Group
from interest.models import Interest
from location.models import Location
from major.models import Major
from prompt.models import Prompt
from purpose.models import Purpose
from push_notifications.models import GCMDevice
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
        profile_pic_url = self._data.get("profile_pic_url")
        profile_pic_base64 = self._data.get("profile_pic_base64")
        facebook_url = self._data.get("facebook_url")
        instagram_username = self._data.get("instagram_username")
        graduation_year = self._data.get("graduation_year")
        pronouns = self._data.get("pronouns")
        purpose_ids = self._data.get("purposes")
        talking_points = self._data.get("talking_points")
        availability = self._data.get("availability")
        location_ids = self._data.get("locations")
        group_ids = self._data.get("groups")
        prompts = self._data.get("prompts")
        interest_ids = self._data.get("interests")
        has_onboarded = self._data.get("has_onboarded")
        pending_feedback = self._data.get("pending_feedback")
        deleted = self._data.get("deleted")
        fcm_registration_token = self._data.get("fcm_registration_token")
        is_paused = self._data.get("is_paused")
        pause_weeks = self._data.get("pause_weeks")

        many_to_many_sets = [
            [Purpose, self._person.purposes, purpose_ids],
            [Major, self._person.majors, major_ids],
            [Location, self._person.locations, location_ids],
            [Group, self._person.groups, group_ids],
            [Interest, self._person.interests, interest_ids],
        ]

        for (class_name, existing_set, ids) in many_to_many_sets:
            possible_error = update_many_to_many_set(class_name, existing_set, ids)
            if possible_error is not None:
                return possible_error

        if not is_paused:
            self._person.pause_expiration = None
            pause_weeks = None

        if pause_weeks is not None:
            if pause_weeks != 0:
                days = pause_weeks * 6
                self._person.pause_expiration = datetime.now() + timedelta(days=days)

        if profile_pic_base64 is not None:
            upload_profile_pic.delay(self._user.id, profile_pic_base64)

        if prompts is not None:
            # Sort prompts by id to ensure Django doesn't change the order
            prompts.sort(key=lambda prompt: prompt.get("id"))

            prompt_questions = []
            prompt_answers = []
            # Now, iterate through prompts to check validity and separate questions/answers
            for prompt in prompts:
                prompt_id = prompt.get("id")
                prompt_answer = prompt.get("answer")
                prompt_question = Prompt.objects.filter(id=prompt_id)
                if not prompt_question:
                    return failure_response(f"Prompt id {prompt_id} does not exist.")
                prompt_questions.append(prompt_id)
                prompt_answers.append(prompt_answer)

            self._person.prompt_questions.set(prompt_questions)
            modify_attribute(self._person, "prompt_answers", json.dumps(prompt_answers))

        if (
            fcm_registration_token is not None
            and self._person.fcm_registration_token != fcm_registration_token
        ):
            GCMDevice.objects.filter(
                registration_id=self._person.fcm_registration_token
            ).delete()
            self._person.fcm_registration_token = fcm_registration_token
            fcm_device = GCMDevice.objects.create(
                registration_id=fcm_registration_token,
                cloud_message_type="FCM",
                user=self._user,
            )
            self._user.fcm_device = fcm_device

        modify_attribute(self._person, "net_id", net_id)
        modify_attribute(self._user, "first_name", first_name)
        modify_attribute(self._user, "last_name", last_name)
        modify_attribute(self._person, "hometown", hometown)
        modify_attribute(self._person, "facebook_url", facebook_url)
        modify_attribute(self._person, "instagram_username", instagram_username)
        modify_attribute(self._person, "graduation_year", graduation_year)
        modify_attribute(self._person, "pronouns", pronouns)
        modify_attribute(self._person, "talking_points", json.dumps(talking_points))
        modify_attribute(self._person, "has_onboarded", has_onboarded)
        modify_attribute(self._person, "pending_feedback", pending_feedback)
        modify_attribute(self._person, "availability", json.dumps(availability))
        modify_attribute(self._person, "profile_pic_url", profile_pic_url)
        modify_attribute(self._person, "soft_deleted", deleted)
        modify_attribute(self._person, "is_paused", is_paused)
        modify_attribute(self._person, "pending_feedback", pending_feedback)
        self._user.save()
        self._person.save()
        return success_response(status=status.HTTP_200_OK)

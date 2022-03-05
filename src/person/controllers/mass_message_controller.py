from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from push_notifications.models import GCMDevice
from rest_framework import status


class MassMessageController:
    def __init__(self, data):
        self._data = data

    def process(self):
        users = self._data.get("users")
        title = self._data.get("title")
        message = self._data.get("message")
        if not users or not title or not message:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        for user_id in users:
            if not User.objects.filter(id=user_id).exists():
                return failure_response(
                    f"User {user_id} does not exist. No notfications sent.",
                    status.HTTP_400_BAD_REQUEST,
                )

        # All user ids in `users` are valid, so we can start sending messages
        message_count = 0
        errors = []
        for user_id in users:
            receiving_user = User.objects.get(id=user_id)
            if receiving_user.person.fcm_registration_token:
                # receiving_user has notfications enabled
                device = GCMDevice.objects.get(
                    registration_id=receiving_user.person.fcm_registration_token
                )
                response = device.send_message(title=title, message=message)
                if response.get("failure") == 1:
                    errors.append(response)
                else:
                    message_count += 1

        if errors:
            return failure_response(
                message=f"{message_count} notifications sent, but {len(errors)} errors occurred: {errors}",
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return success_response(
            data=f"{message_count} notifications sent, {len(users)-message_count} users do not have push notifications enabled",
            status=status.HTTP_201_CREATED,
        )

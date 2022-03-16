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
        # if sandbox=True, don't send messages - just check who has notifs
        # enabled. if sandbox=False or is not set, then send messages
        sandbox = self._data.get("sandbox")
        if not users or not title or not message:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )
        if sandbox is not None and type(sandbox) != bool:
            return failure_response(
                "sandbox must be a boolean", status.HTTP_400_BAD_REQUEST
            )
        for user_id in users:
            if not User.objects.filter(id=user_id).exists():
                return failure_response(
                    f"User {user_id} does not exist. No notfications sent.",
                    status.HTTP_400_BAD_REQUEST,
                )

        # All user ids in `users` are valid, so we can start sending messages
        message_count = 0
        notifs_enabled_count = 0
        errors = []
        for user_id in users:
            receiving_user = User.objects.get(id=user_id)
            if receiving_user.person.fcm_registration_token:
                # receiving_user has notfications enabled
                if sandbox:
                    # don't send any messages
                    notifs_enabled_count += 1
                else:
                    # sandbox=False or None, so try to send the message
                    device = GCMDevice.objects.get(
                        registration_id=receiving_user.person.fcm_registration_token
                    )
                    firebase_response = device.send_message(
                        title=title, message=message
                    )
                    if firebase_response.get("failure") == 1:
                        errors.append(firebase_response)
                    else:
                        message_count += 1

        if sandbox:
            # no messages were sent
            return success_response(
                data=f"{notifs_enabled_count} users have push notifications enabled, no notfications sent (sandbox mode)",
                status=status.HTTP_200_OK,
            )
        else:
            # sandbox=False or None, so we tried to send messages
            if errors:
                return failure_response(
                    message=f"{message_count} notifications sent, but {len(errors)} errors occurred: {errors}",
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            return success_response(
                data=f"{message_count} notifications sent, {len(users)-message_count} users do not have push notifications enabled",
                status=status.HTTP_201_CREATED,
            )

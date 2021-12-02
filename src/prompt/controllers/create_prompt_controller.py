from api.utils import failure_response
from api.utils import success_response
from prompt.models import Prompt
from rest_framework import status


class CreatePromptController:
    def __init__(self, data, serializer):
        self._data = data
        self._serializer = serializer

    def process(self):
        # Verify that all required fields are provided
        name = self._data.get("question_name")
        if name is None:
            return failure_response(
                "POST body is misformatted", status.HTTP_400_BAD_REQUEST
            )

        # Get label field
        label = self._data.get("question_placeholder")

        # Check if a prompt already exists with the given fields and return it if so
        prompt = Prompt.objects.filter(question_name=name, question_placeholder=label)
        if prompt:
            return success_response(
                self._serializer(prompt[0]).data, status.HTTP_200_OK
            )

        # Create and return a new prompt with the given fields
        prompt = Prompt.objects.create(question_name=name, question_placeholder=label)
        prompt.save()
        return success_response(self._serializer(prompt).data, status.HTTP_201_CREATED)

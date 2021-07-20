from prompt.models import Prompt


class PopulatePromptController:
    def __init__(self, data):
        self._name = data[0]
        self._label = data[1]

    def process(self):
        # Check if a prompt already exists with the given fields and return False if so
        prompt = Prompt.objects.filter(
            question_name=self._name, label_users_see=self._label
        )
        if prompt:
            return False

        # Return True after creating a new prompt with the given fields
        prompt = Prompt.objects.create(
            question_name=self._name, label_users_see=self._label
        )
        prompt.save()
        return True

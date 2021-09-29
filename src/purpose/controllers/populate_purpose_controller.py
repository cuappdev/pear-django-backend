from purpose.models import Purpose


class PopulatePurposeController:
    def __init__(self, data):
        self._name = data[0]

    def process(self):
        # Check if a purpose already exists with the given fields and return False if so
        purpose = Purpose.objects.filter(name=self._name)
        if purpose:
            return False

        # Return True after creating a new purpose with the given fields
        purpose = Purpose.objects.create(name=self._name)
        purpose.save()
        return True

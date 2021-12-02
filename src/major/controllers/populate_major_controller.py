from major.models import Major


class PopulateMajorController:
    def __init__(self, data):
        self._name = data[0]

    def process(self):
        # Check if a major already exists with the given fields and return False if so
        major = Major.objects.filter(name=self._name)
        if major:
            return False

        # Return True after creating a new major with the given fields
        major = Major.objects.create(name=self._name)
        major.save()
        return True

from group.models import Group


class PopulateGroupController:
    def __init__(self, data):
        self._name = data[0]
        self._subtitle = data[1]
        self._img_url = data[2]

    def process(self):
        # Check if a group already exists with the given fields and return False if so
        group = Group.objects.filter(
            name=self._name, subtitle=self._subtitle, img_url=self._img_url
        )
        if group:
            return False

        # Return True after creating a new group with the given fields
        group = Group.objects.create(
            name=self._name, subtitle=self._subtitle, img_url=self._img_url
        )
        group.save()
        return True

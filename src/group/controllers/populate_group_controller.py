from group.models import Group
from pear import settings


class PopulateGroupController:
    def __init__(self, data):
        self._name = data[0]
        self._subtitle = data[1]
        # This is a temporary measure until our upload service has been updated
        image_tag = settings.DEFAULT_GROUP_IMAGE_TAG if data[2] == "" else data[2]
        self._img_url = settings.IMAGE_HOST_BASE + image_tag

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

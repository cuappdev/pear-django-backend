from group.models import Group


class PopulateGroupController:
    def __init__(self, data):
        self._name = data[0]

    def process(self):
        """Populate groups from a line of a text file. Returns True after
        creating a Group if the datum in the data describes a unique Group."""
        group = Group.objects.filter(name=self._name)
        if group:
            return False
        new_group = Group.objects.create(name=self._name)
        new_group.save()
        return True

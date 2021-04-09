from location.models import Location


class PopulateLocationController:
    def __init__(self, data):
        self._area = data[0]
        self._name = data[1]

    def process(self):
        """Populate locations from a line of a text file. Returns True after
        creating a Location if the datum in the data describes a unique Location."""
        location = Location.objects.filter(name=self._name, area=self._area)
        if location:
            return False
        else:
            new_location = Location.objects.create(name=self._name, area=self._area)
            new_location.save()
            return True

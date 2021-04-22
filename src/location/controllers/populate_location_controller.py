from location.models import Location


class PopulateLocationController:
    def __init__(self, data):
        self._area = data[0]
        self._name = data[1]

    def process(self):
        """Process a request to populate the database with location
        data. Returns True for newly created unique locations and
        False if a location with the given data exists already."""

        # Check if a location already exists with the given fields and return False if so
        location = Location.objects.filter(name=self._name, area=self._area)
        if location:
            return False

        # Return True after creating a new location with the given fields
        location = Location.objects.create(name=self._name, area=self._area)
        location.save()
        return True

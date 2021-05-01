from interest.models import Interest


class PopulateInterestController:
    def __init__(self, data):
        self._name = data[0]
        self._subtitle = data[1]
        self._img_url = data[2]

    def process(self):
        # Check if a interest already exists with the given fields and return False if so
        interest = Interest.objects.filter(
            name=self._name, subtitle=self._subtitle, img_url=self._img_url
        )
        if interest:
            return False

        # Return True after creating a new interest with the given fields
        interest = Interest.objects.create(
            name=self._name, subtitle=self._subtitle, img_url=self._img_url
        )
        interest.save()
        return True

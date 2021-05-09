from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_times_list(items):
    """Validates a timestamps list. Ensures every element in items is a valid
    availability for a day, which should be a list (without brackets) of floats.
    Valid example: ["0,1", "18.5,19.5","","", "12", "0,1", "0,1,3,4,5"]
    Precondition: items is a list of strings"""
    for element in items:
        nested_list = element.strip().split(",")
        if not all(isinstance(element, float) for element in nested_list):
            raise ValidationError(
                _(f"{items} is not a valid list of timestamps"),
                params={"items": items},
            )


def validate_int_list(items):
    """Precondition: items is a list"""
    if not all(isinstance(element, int) for element in items):
        raise ValidationError(
            _(f"{items} is not an int list"),
            params={"items": items},
        )

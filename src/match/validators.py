from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_times_list(value):
    updated_list = []
    for value_element in value:
        try:
            nested_list = value_element.strip().split(",")
            for index in range(len(nested_list)):
                if nested_list[index] != "":
                    nested_list[index] = float(nested_list[index])
            updated_list.append(str(nested_list)[1:-1])
        except (ValueError, TypeError):
            raise ValidationError(
                _(f"{value} is not a valid list of times"),
                params={"value": value},
            )
    value = updated_list


def validate_int_list(value):
    updated_list = []
    for value_element in value:
        try:
            updated_list.append(int(value_element))
        except (ValueError, TypeError):
            raise ValidationError(
                _(f"{value} is not an int list"),
                params={"value": value},
            )
    value = updated_list

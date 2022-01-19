from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, status=status.HTTP_200_OK):
    """Returns a Response with `status` (200 default) and `data` if provided."""
    if data is None:
        return Response({"success": True}, status=status)
    return Response({"success": True, "data": data}, status=status)


def failure_response(message=None, status=status.HTTP_404_NOT_FOUND):
    """Returns a Response with `status` (404 default) and `message` if provided."""
    if message is None:
        return Response({"success": False}, status=status)
    return Response({"success": False, "error": message}, status=status)


def success_response_with_query(query, data, status=status.HTTP_200_OK):
    """Returns a Response with `query`, `data`, and `status` (200 default)."""
    return Response({"success": True, "query": query, "data": data}, status=status)


def failure_response_with_query(query, message, status=status.HTTP_404_NOT_FOUND):
    """Returns a Response with `query`, `message`, and `status` (404 default)."""
    return Response({"success": False, "query": query, "error": message}, status=status)


def modify_attribute(model, attr_name, attr_value):
    """Modify an attribute if it isn't None and has been changed."""
    if (
        attr_value is not None
        and attr_value != "null"
        and attr_value != getattr(model, attr_name)
    ):
        setattr(model, attr_name, attr_value)


def update_many_to_many_set(class_name, existing_set, ids):
    """Update a ManyToMany relation set for a person object (i.e. Locations, Groups, etc)"""
    if ids is not None:
        new_objects = []
        for id in ids:
            new_object = class_name.objects.filter(id=id)
            if not new_object:
                return failure_response(
                    f"{class_name.__name__} id {id} does not exist."
                )
            new_objects.append(new_object[0])
        existing_set.set(new_objects)

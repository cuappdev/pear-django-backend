from api.utils import failure_response
from api.utils import success_response
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from rapidfuzz import process as fuzzymatch
from rest_framework import status


class SearchPersonController:
    def __init__(self, request, serializer):
        self._request = request
        self._data = request.data
        self._serializer = serializer

    def process(self):
        users = User.objects.filter(
            Q(person__has_onboarded=True) & Q(person__soft_deleted=False)
        )
        query = self._data.get("query")
        # Check if query was provided and isn't whitespace
        if query is not None and query.strip() != "":
            # Create processor to ignore query but convert User object into string choice
            def user_properties(user):
                return [user.first_name.lower(), user.last_name.lower()]

            def processor(user):
                return user if type(user) is str else " ".join(user_properties(user))

            searched_users = fuzzymatch.extract(
                query.lower(), users, processor=processor
            )
            # Extract the users from the returned tuple list
            users = list(map(lambda searched_user: searched_user[0], searched_users))

        page_size = self._data.get("page_size")
        page_number = self._data.get("page_number")
        if page_size is not None and page_number is not None:
            paginator = Paginator(users, page_size)
            try:
                page = paginator.page(page_number)
                users = page.object_list
            except:
                return failure_response("Page not found", status.HTTP_404_NOT_FOUND)
        return success_response(
            self._serializer(
                users, context={"request_user": self._request.user}, many=True
            ).data,
            status.HTTP_200_OK,
        )

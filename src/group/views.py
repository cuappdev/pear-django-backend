import json

from api import settings as api_settings
from api.utils import failure_response
from api.utils import success_response
from group.models import Group
from rest_framework import generics
from rest_framework import status

from .controllers.create_group_controller import CreateGroupController
from .controllers.update_group_controller import UpdateGroupController
from .serializers import GroupSerializer


class GroupsView(generics.GenericAPIView):
    serializer_class = GroupSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request):
        """Get all groups."""
        groups = Group.objects.all()
        return success_response(
            self.serializer_class(groups, many=True).data, status.HTTP_200_OK
        )

    def post(self, request):
        """Create a group."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return CreateGroupController(data, self.serializer_class).process()


class GroupView(generics.GenericAPIView):
    serializer_class = GroupSerializer
    permission_classes = api_settings.CONSUMER_PERMISSIONS

    def get(self, request, id):
        """Get group by id."""
        group = Group.objects.filter(id=id)
        if not group:
            return failure_response("Group does not exist", status.HTTP_404_NOT_FOUND)
        return success_response(
            self.serializer_class(group[0]).data, status.HTTP_200_OK
        )

    def post(self, request, id):
        """Update group by id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.data
        return UpdateGroupController(id, data, self.serializer_class).process()

    def delete(self, request, id):
        """Delete a group by id."""
        group = Group.objects.filter(id=id)
        if not group:
            return failure_response("Group does not exist", status.HTTP_404_NOT_FOUND)
        group[0].delete()
        return success_response(
            self.serializer_class(group[0]).data, status.HTTP_200_OK
        )

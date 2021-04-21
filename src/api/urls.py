from api.views import CountdownDummyView
from api.views import PopulateView
from django.urls import path
from group.views import GroupsView
from group.views import GroupView
from interest.views import InterestsView
from location.views import LocationsView
from location.views import LocationView
from match.views import CurrentMatchView
from match.views import MatchesView
from match.views import MatchView
from person.views import AuthenticateView
from person.views import MeView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("me/", MeView.as_view(), name="me"),
    path("interests/", InterestsView.as_view(), name="interests"),
    path("groups/", GroupsView.as_view(), name="groups"),
    path("groups/<int:id>/", GroupView.as_view(), name="group"),
    path("locations/", LocationsView.as_view(), name="locations"),
    path("locations/<int:id>/", LocationView.as_view(), name="location"),
    path("matches/", MatchesView.as_view(), name="matches"),
    path("matches/<int:id>/", MatchView.as_view(), name="match"),
    path("matches/current/", CurrentMatchView.as_view(), name="current_match"),
    path("populate/", PopulateView.as_view(), name="populate"),
    path("countdown/", CountdownDummyView.as_view(), name="countdown"),
]

from api.views import CountdownDummyView
from api.views import PopulateView
from django.urls import path
from group.views import GroupsView
from group.views import GroupView
from interest.views import InterestsView
from interest.views import InterestView
from location.views import LocationsView
from location.views import LocationView
from major.views import MajorsView
from major.views import MajorView
from match.views import AlgorithmView
from match.views import AllMatchesView
from match.views import CancelCurrentMatchView
from match.views import CancelMatchView
from match.views import CurrentMatchView
from match.views import MatchView
from match.views import MultipleMatchesView
from match.views import MyMatchesView
from match.views import UserMatchesView
from person.views import AuthenticateView
from person.views import BlockUserView
from person.views import MassMessageView
from person.views import MeView
from person.views import PingView
from person.views import SendMessageView
from person.views import UnblockUserView
from person.views import UsersView
from person.views import UserView
from prompt.views import PromptsView
from prompt.views import PromptView
from purpose.views import PurposesView
from purpose.views import PurposeView
from survey.views import AllSurveysView
from survey.views import SurveysView
from survey.views import SurveyView


urlpatterns = [
    # User URLs
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("me/", MeView.as_view(), name="me"),
    path("me/ping/", PingView.as_view(), name="ping"),
    path("users/", UsersView.as_view(), name="users"),
    path("users/<int:id>/", UserView.as_view(), name="user"),
    path("users/<int:id>/block/", BlockUserView.as_view(), name="block_user"),
    path("users/<int:id>/unblock/", UnblockUserView.as_view(), name="unblock_user"),
    path("users/<int:id>/matches/", UserMatchesView.as_view(), name="user_matches"),
    # Push Notification URLs
    path("users/<int:id>/message/", SendMessageView.as_view(), name="user_messages"),
    path("mass-message/", MassMessageView.as_view(), name="user_messages"),
    # Interest URLs
    path("interests/", InterestsView.as_view(), name="interests"),
    path("interests/<int:id>/", InterestView.as_view(), name="interest"),
    # Group URLs
    path("groups/", GroupsView.as_view(), name="groups"),
    path("groups/<int:id>/", GroupView.as_view(), name="group"),
    # Location URLs
    path("locations/", LocationsView.as_view(), name="locations"),
    path("locations/<int:id>/", LocationView.as_view(), name="location"),
    # Major URLs
    path("majors/", MajorsView.as_view(), name="majors"),
    path("majors/<int:id>/", MajorView.as_view(), name="major"),
    # Purpose URLs
    path("purposes/", PurposesView.as_view(), name="purposes"),
    path("purposes/<int:id>/", PurposeView.as_view(), name="purpose"),
    # Match URLs
    path("matches/", MyMatchesView.as_view(), name="matches"),
    path("matches/algorithm/", AlgorithmView.as_view(), name="algorithm"),
    path("matches/all/", AllMatchesView.as_view(), name="all_matches"),
    path("matches/multiple/", MultipleMatchesView.as_view(), name="multiple_matches"),
    path("matches/<int:id>/", MatchView.as_view(), name="match"),
    path("matches/<int:id>/cancel/", CancelMatchView.as_view(), name="cancel_match"),
    path("matches/current/", CurrentMatchView.as_view(), name="current_match"),
    path(
        "matches/current/cancel/",
        CancelCurrentMatchView.as_view(),
        name="cancel_current_match",
    ),
    # Survey/Feedback URLs
    path("matches/feedback/", AllSurveysView.as_view(), name="surveys"),
    path("match/<int:match_id>/feedback/", SurveysView.as_view(), name="match_surveys"),
    path(
        "match/<int:match_id>/feedback/<int:id>/",
        SurveyView.as_view(),
        name="match_survey",
    ),
    # Prompt URLs
    path("prompts/", PromptsView.as_view(), name="prompts"),
    path("prompts/<int:id>/", PromptView.as_view(), name="prompt"),
    # Other
    path("populate/", PopulateView.as_view(), name="populate"),
    path("countdown/", CountdownDummyView.as_view(), name="countdown"),
]

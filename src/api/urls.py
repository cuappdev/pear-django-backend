from api.views import CountdownDummyView
from api.views import PopulateView
from django.urls import path
from interest.views import InterestsView
from location.views import LocationsView
from person.views import AuthenticateView
from person.views import MeView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("me/", MeView.as_view(), name="me"),
    path("interests/", InterestsView.as_view(), name="interests"),
    path("locations/", LocationsView.as_view(), name="locations"),
    path("populate/", PopulateView.as_view(), name="populate"),
    path("countdown/", CountdownDummyView.as_view(), name="countdown"),
]

from api.views import PopulateView
from django.urls import path
from interest.views import InterestsView
from person.views import AuthenticateView
from person.views import MeView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("me/", MeView.as_view(), name="me"),
    path("interests/", InterestsView.as_view(), name="interests"),
    path("populate/", PopulateView.as_view(), name="populate"),
]

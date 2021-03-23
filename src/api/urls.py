from api.views import PopulateView
from django.urls import path
from interest.views import InterestsView
from person.views import AuthenticateView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("interests/", InterestsView.as_view(), name="interests"),
    path("populate/", PopulateView.as_view(), name="populate"),
]

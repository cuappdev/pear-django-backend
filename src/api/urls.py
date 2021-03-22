from django.urls import path
from interest.views import InterestAllView
from person.views import AuthenticateView


urlpatterns = [
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("interests/", InterestAllView.as_view(), name="interests"),
]

from django.urls import path

from apps.authentication.api import LoginApi, RegistrationApi

urlpatterns = [
    path("signup/", RegistrationApi.as_view()),
    path("signin/", LoginApi.as_view()),
    # path("signout", Logout.asview()),
]

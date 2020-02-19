from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("signUp/", views.signUp, name="signUp"),
    path("events/", views.events, name="events"),
    path("CreateEvent/", views.events, name="createEvent"),
    path("profile/", views.events, name="profile"),
    path("signUp/", views.events, name="SignUp"),
    path("logIn/", views.events, name="logIn")
]

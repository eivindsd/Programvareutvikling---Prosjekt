from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name="home"),
    path("events/", views.events, name="events"),
    path("CreateEvent/", views.events, name="createEvent"),
    path("profile/", views.events, name="profile"),
    path("signUp/", user_views.register, name="signUp"),
    path("logIn/", views.events, name="logIn")
]

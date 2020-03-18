from django.urls import path
from . import views
from users import views as user_views

"""Creates the url path to the different templates, sends the request to 'views' file"""

urlpatterns = [
    path('', views.startPage, name="startPage"),
    path("events/", views.events, name="events"),
    path("createEvent/", views.createEvent, name="createEvent"),
    path("profile/", views.events, name="profile"),
    path("signUp/", user_views.register, name="signUp"),
    path("logIn/", user_views.login, name="logIn"),
    path("home/", views.home, name="home"),
    path("createPost/", views.createPost, name="createPost"),
    path("messages/", views.message, name="messages"),
]


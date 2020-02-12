from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="blog-home"), #views.home refererer til home funksjonen i blog.views, som sender informasjonen til klienten
    path("about/", views.about, name="blog-about")
]

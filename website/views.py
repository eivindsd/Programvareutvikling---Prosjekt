from django.shortcuts import render, redirect
from website.models import Arrangement

from website.models import Arrangement


def home(request):
    if not request.user.is_authenticated:
        return redirect('startPage')
    return render(request, "website/home.html")



"""
def signUp(request):
    return render(request, "website/signUp.html")
"""


def events(request):
    #change this to see all and mine
    contex = {
        'arrangementer': Arrangement.get_all(Arrangement)
    }
    return render(request, "website/events.html", contex)


def startPage(request):
    if request.user.is_authenticated:
         return redirect('profile')
    return render(request, "website/startPage.html")


def profile(request):
    return render(request, "website/profile.html")


def createEvent(request):
    return render(request, "website/createEvent.html")

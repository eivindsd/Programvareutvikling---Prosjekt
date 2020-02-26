from django.shortcuts import render, redirect

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
    contex = {
        'arrangementer': Arrangement.objects.all()
    }
    return render(request, "website/events.html", contex)


def startPage(request):
    return render(request, "website/startPage.html")



def logIn(request):
    return render(request, "website/logIn.html")


def profile(request):
    return render(request, "website/profile.html")


def createEvent(request):
    return render(request, "website/createEvent.html")

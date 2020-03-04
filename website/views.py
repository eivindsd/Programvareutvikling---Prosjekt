from django.shortcuts import render, redirect
from users.forms import eventFormAdmin, eventFormBedrift, eventFormBruker
from django.contrib import messages
from website.models import Arrangement

"""Loads the correct template and form (when needed)"""

def home(request):
    if not request.user.is_authenticated:
        return redirect('startPage')
    return render(request, "website/home.html")


def events(request):
    #change this to see all and mine
    if request.method == 'POST':
        print("Meld deg på! Request: {} ".format(request.POST.get('arr')))
    contex = {
        'arrangementer': Arrangement.get_all(Arrangement),
        'user' : request.user
    }
    return render(request, "website/events.html", contex)


def startPage(request):
    if request.user.is_authenticated:
         return redirect('profile')
    return render(request, "website/startPage.html")


def profile(request):
    return render(request, "website/profile.html")


def createEvent(request):
    if request.method == 'POST':
        if request.user:
            if request.user.get_bruker_type() == 'admin':
                form = eventFormAdmin(request.POST, user=request.user)
            elif request.user.get_bruker_type() == 'bedrift':
                form = eventFormBedrift(request.POST, user=request.user)
            else:
                form = eventFormBruker(request.POST, user=request.user)
        else:
            print("Error user!")
            return False
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            type_select = form.cleaned_data.get('type_select')
            messages.success(request, f'{type_select} opprettet for {title}')
            return redirect('events')
    else:
        if request.user:
            if request.user.get_bruker_type() == 'admin':
                form = eventFormAdmin(user=request.user)
            elif request.user.get_bruker_type() == 'bedrift':
                form = eventFormBedrift(user=request.user)
            else:
                form = eventFormBruker(user=request.user)
    return render(request, "website/createEvent.html", {'form': form})


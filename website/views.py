from django.shortcuts import render, redirect
from users.forms import eventFormAdmin, eventFormBedrift, eventFormBruker, postForm
from django.contrib import messages
from website.models import Arrangement, deltokArrangement

"""Loads the correct template and form (when needed)"""

def home(request):
    if not request.user.is_authenticated:
        return redirect('startPage')
    return render(request, "website/home.html")


def events(request):
    #change this to see all and mine
    if request.method == 'POST':
        arrId = request.POST.get('arrId')
        if request.POST.get('meldPaa') != None:
            participated = deltokArrangement.objects.participate(request.user, arrId)
            if participated == False:
                messages.error(request, f'Du er allerede meldt på dette arrangementet!')
        elif request.POST.get('meldAv') != None:
            deleted = deltokArrangement.objects.unregister(request.user, arrId)
            if deleted == False:
                messages.error(request, f'Fant ikke dette arrangementet!')

    alleDeltok = deltokArrangement.getMyArrangementId(deltokArrangement, request.user)
    contex = {
        'arrangementer': Arrangement.get_all(Arrangement),
        'user': request.user,
        'alledeltok': alleDeltok,
    }
    return render(request, "website/events.html", contex)


def startPage(request):
    if request.user.is_authenticated:
         return redirect('profile')
    return render(request, "website/startPage.html")


def profile(request):
    contex = {}
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


def createPost(request):
    if request.method == 'POST':
        form = postForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = postForm()
    return render(request, "website/createPost.html", {'form': form})

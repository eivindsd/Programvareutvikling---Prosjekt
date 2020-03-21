from django.shortcuts import render, redirect
from users.forms import eventFormAdmin, eventFormBedrift, eventFormBruker, postForm, eventForm, sendMessageForm, AllUsersForm
from django.contrib import messages
from website.models import Arrangement, deltokArrangement, Messages, Bruker, innlegg

"""Loads the correct template and form (when needed)"""

def home(request):
    if not request.user.is_authenticated:
        return redirect('startPage')
    if request.method == 'POST':
        form = AllUsersForm(request.POST, user=request.user)
        """Se andres profil"""
        IDs = request.POST.getlist('bruker')
        if len(IDs) > 0:
            userId = request.POST.getlist('bruker')[0]
        else: userId = False
        if userId:
            user = Bruker.get_user_by_id(Bruker, int(userId))
            contex = {"Arrangementer": Arrangement.getMyArrangement(Arrangement, user),
                      "Innlegg": innlegg.getMyPosts(innlegg, user),
                      "user": user,
                      }
            return render(request, "users/otherProfile.html", contex)
        """Svar på meldingen"""
        if request.POST.get("svar"):
            messageId = request.POST.get("messageId")
            answerText = request.POST.get("svarText")
            if answerText == "":
                messages.warning(request, f'Du har glemt å skrive svaret!')
            else:
                Messages.objects.answer(answerText, messageId)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AllUsersForm(request.user)
    contex = {
        'mineMeldinger': Messages.getMyMessages(Messages, request.user),
        'form': form,
        'brukere': Bruker.get_all(Bruker),
        'svarene': Messages.myAnsweredMessages(Messages, request.user),
    }
    return render(request, "website/home.html", contex)


def events(request):
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



def createEvent(request):
    if request.method == 'POST':
        if request.POST.get('opprett') == None:
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
    else:
        form = eventForm(user=request.user)
    return render(request, "website/createEvent.html", {'form': form})


def createPost(request):
    if request.method == 'POST':
        if request.POST.get('nytt') == None:
            form = postForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else: form = postForm()
    else:
        form = postForm()
    return render(request, "website/createPost.html", {'form': form})


def message(request):
    if request.method == 'POST':
        if request.POST.get('SendMessageForm') == None:
            form = sendMessageForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else: form = sendMessageForm(user=request.user)
    else:
        form = sendMessageForm(user=request.user)
    if not request.user.is_authenticated:
        return redirect('startPage')
    return render(request, "website/messages.html", {"form": form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import Arrangement, innlegg
from .forms import UserRegisterForm

"""Redirects an url-request to the correct html-template, also displays the appropriate form if needed"""

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    contex = {"mineArrangementer": Arrangement.getMyArrangement(Arrangement, request.user),
              "mineInnlegg": innlegg.getMyPosts(innlegg, request.user)}
    return render(request, "users/profile.html", contex)

def login(request):
    return render(request, 'users/login.html')

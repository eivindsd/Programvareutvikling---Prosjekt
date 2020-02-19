from django import forms
#from django.contrib.auth.models import User
from website.models import Rolle, Bruker
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailInput() #Leaving this blanck will set this as a required field

    class Meta:
        model = Bruker
        fields = ['brukerNavn', 'epost', 'password1', 'password2']

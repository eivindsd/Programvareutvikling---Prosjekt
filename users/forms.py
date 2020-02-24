from django import forms
#from django.contrib.auth.models import User
from website.models import Rolle, Bruker
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    #email = forms.EmailInput() #Leaving this blanck will set this as a required field
    bedrift = forms.BooleanField(widget=forms.CheckboxInput(), label="Er du en Bedrift", required=False)
    vanligBruker = forms.BooleanField(widget=forms.CheckboxInput(), label="Er du en vanlig Bruker", required=False)

    class Meta:
        model = Bruker
        fields = ['username', 'email', 'password1', 'password2', 'bedrift', 'vanligBruker']

    def clean(self):
        print(self.data)
        print(self.errors)
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        return cleaned_data

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        # email, password1 = v['email'], v['password1']
        bruker = None
        if data['bedrift']:
            bruker = Bruker.objects.create_bedrift(
            username=data['username'],
            email=data['email'],
            password=data['password1'],)
        elif data['vanligBruker']:
            bruker = Bruker.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],)
        # User is already saved after calling BaseUserManager function.
        return bruker
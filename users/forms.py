from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.forms import DateInput
from django.utils.translation import gettext, gettext_lazy as _
from website.models import Rolle, Bruker
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    #email = forms.EmailInput() #Leaving this blanck will set this as a required field
    error_messages = {
        'password_mismatch': _('De to passordfeltene stemte ikke.'),
    }
    email = forms.EmailField(label=_("Epost"), required=True)
    password1 = forms.CharField(
        label=_("Passord"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=("Passordet ditt kan ikke være for likt den andre personlige informasjonen din."
                   "\nPassordet ditt må inneholde minst 8 tegn.\n"
                   "Passordet ditt kan ikke være et ofte brukt passord.\n"
                   "Passordet ditt kan ikke være helt numerisk."),
    )
    password2 = forms.CharField(
        label=_("Passord bekreftelse"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Skriv inn det samme passordet som før, for bekreftelse."),
    )
    bedrift = forms.BooleanField(widget=forms.CheckboxInput(), label="Er du en Bedrift", required=False)
    vanligBruker = forms.BooleanField(widget=forms.CheckboxInput(), label="Er du en vanlig Bruker", required=False)
    strikkeNivaa = forms.IntegerField(label="strikkeNivå", required=False, help_text=_("Ditt strikke nivå av 100."),)
    bursdag = forms.DateField(required=False, label="Fødselsdato", input_formats=['%d/%m/%Y'],
                              help_text=_("dd/mm/åååå"),)
    fornavn = forms.CharField(label='Fornavn')
    etternavn = forms.CharField(label='Etternavn')

    class Meta:
        model = Bruker
        fields = ['fornavn', 'etternavn', 'username', 'email', 'password1', 'password2', 'bedrift', 'vanligBruker', 'strikkeNivaa', 'bursdag']

    def clean(self):
        print(self.data)
        print(self.errors)
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        return cleaned_data

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        bruker = None
        if data['bedrift']:
            bruker = Bruker.objects.create_bedrift(
                username=data['username'],
                email=data['email'],
                password=data['password1'],
                first_name=data['fornavn'],
                last_name=data['etternavn'],
                bursdag=data['bursdag'],
                strikkeNivaa=data['strikkeNivaa'],)
        else:
            bruker = Bruker.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password1'],
                first_name=data['fornavn'],
                last_name=data['etternavn'],
                bursdag=data['bursdag'],
                strikkeNivaa=data['strikkeNivaa'],)


        # User is already saved after calling BaseUserManager function.
        return bruker
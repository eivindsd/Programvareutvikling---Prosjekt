from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.forms import DateInput
from django.utils.translation import gettext, gettext_lazy as _
from website.models import Rolle, Bruker, Arrangement, ArrangementManager
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    #email = forms.EmailInput() #Leaving this blanck will set this as a required field
    error_messages = {
        'password_mismatch': _('De to passordfeltene stemte ikke.'),
    }
    email = forms.EmailField(label=_("E-post"), required=True)
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
        label=_("Bekreft ditt passord"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Gjenta passordet ditt for bekreftelse."),
    )
    bedrift = forms.BooleanField(widget=forms.CheckboxInput(), label="Jeg er en bedrift", required=False)
    vanligBruker = forms.BooleanField(widget=forms.CheckboxInput(), label="Jeg er en privatperson", required=False)
    strikkeNivaa = forms.IntegerField(label="Ditt strikkenivå", required=False, help_text=_("Ditt strikkenivå; 0-100."),)
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


class eventForm(forms.ModelForm):
    title = forms.CharField(label="Tittel", strip=False)
    time = forms.DateTimeField(label='Tidspunkt', input_formats=['%d/%m/%Y %H:%M'], help_text='dd/mm/åååå tt:mm')
    location = forms.CharField(label='Sted')
    text = forms.CharField(widget=forms.Textarea, label='Beskrivelse')

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'location', 'text')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def getUser(self):
        current_user = self.user #Should return the user currently logged in
        return current_user

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        if data['type_select'] == 'strikkekveld':
            arrangement = Arrangement.objects.create_strikkeKveld(
                title=data['title'],
                innhold=data['text'],
                forfatter=self.getUser(),
                tidspunkt=data['time'])
        elif data['type_select'] == 'kurs':
            arrangement = Arrangement.objects.create_Kurs(
                title=data['title'],
                innhold=data['text'],
                forfatter=self.getUser(),
                tidspunkt=data['time'])
        else:
            arrangement = Arrangement.objects.create_utfordring(
                title=data['title'],
                innhold=data['text'],
                forfatter=self.getUser(),
                tidspunkt=data['time']
            )
        return arrangement

class eventFormAdmin(eventForm):
    CHOICES = [('strikkekveld', 'strikkekveld'),
               ('kurs', 'kurs'),
               ('utfordring', 'utfordring')]
    type_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'type_select', 'location', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class eventFormBedrift(eventForm):
    CHOICES = [('kurs', 'kurs'), ('utfordring', 'utfordring')]
    type_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'type_select', 'location', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class eventFormBruker(eventForm):
    CHOICES = [('strikkekveld', 'strikkekveld')]
    type_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'type_select', 'location', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
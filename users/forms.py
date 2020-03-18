from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from website.models import Bruker, Arrangement, innlegg
from website.models import Bruker, Arrangement, Messages
from django.contrib.auth.forms import UserCreationForm

"""Class for the different forms used on the site"""

class UserRegisterForm(UserCreationForm):
    """Form to register the user"""

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
    CHOICES = [('bedrift', 'Jeg er en bedrift'),
               ('vanligBruker', 'Jeg er en privatperson'),]
    type_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    strikkeNivaa = forms.IntegerField(label="Ditt strikkenivå", required=False, help_text=_("Ditt strikkenivå; 0-100."),)
    bursdag = forms.DateField(required=False, label="Fødselsdato", input_formats=['%d/%m/%Y'],
                              help_text=_("dd/mm/åååå"),)
    fornavn = forms.CharField(label='Fornavn')
    etternavn = forms.CharField(label='Etternavn')

    class Meta:
        model = Bruker
        fields = ['fornavn', 'etternavn', 'username', 'email', 'password1', 'password2', 'type_select', 'strikkeNivaa', 'bursdag']

    def clean(self):
        """Validates the data input from the form"""
        print(self.data)
        print(self.errors)
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        return cleaned_data

    def save(self, *args, **kwargs):
        """Creates the correct user type and stores it in the database"""
        data = self.cleaned_data
        if data['type_select'] == 'bedrift':
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
    """Form to create an event"""

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
        """Returns the user who is currently logged in"""
        current_user = self.user
        return current_user

    def save(self, *args, **kwargs):
        """Creates the correct event-type and stores it in the database"""
        data = self.cleaned_data  #Gets the data from the form, stores it as a dict
        if data['type_select'] == 'strikkekveld':
            arrangement = Arrangement.objects.create_strikkeKveld(
                title=data['title'],
                innhold=data['text'],
                forfatter=self.getUser(),
                tidspunkt=data['time'],
                location=data['location'])
        elif data['type_select'] == 'kurs':
            arrangement = Arrangement.objects.create_kurs(
                title=data['title'],
                innhold=data['text'],
                forfatter=self.getUser(),
                tidspunkt=data['time'],
                location=data['location'])
        else:
            arrangement = Arrangement.objects.create_utfordring(
                title=data['title'],
                innhold=data['text'],
                forfatter=self.getUser(),
                tidspunkt=data['time'],
                location=data['location']
            )
        return arrangement

class eventFormAdmin(eventForm):
    """Setup for the event form for an admin user"""
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
    """Setup for the event form for an Bedrift user"""
    CHOICES = [('kurs', 'kurs'), ('utfordring', 'utfordring')]
    type_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'type_select', 'location', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class eventFormBruker(eventForm):
    """Setup for the event form for an ordinary user"""
    CHOICES = [('strikkekveld', 'strikkekveld')]
    type_select = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'type_select', 'location', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class showArrangementerForm(forms.ModelForm):
    """This form has to be fixed"""
    title = forms.CharField(label="Tittel", strip=False)
    time = forms.DateTimeField(label='Tidspunkt', input_formats=['%d/%m/%Y %H:%M'], help_text='dd/mm/åååå tt:mm')
    location = forms.CharField(label='Sted')
    text = forms.CharField(widget=forms.Textarea, label='Beskrivelse')

    class Meta():
        model = Arrangement
        fields = ('title', 'time', 'location', 'text')
        readonly = ('title', 'time', 'location', 'text')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class postForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea, label='Tekst')

    class Meta():
        model = innlegg
        fields = ('text',)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def getUser(self):
        """Returns the user who is currently logged in"""
        current_user = self.user
        return current_user

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        nyInnlegg = innlegg(text=data['text'], bruker=self.getUser())
        nyInnlegg.save()



class sendMessageForm(forms.ModelForm):
    """Form to create and send message"""
    ##må jeg lage post-metode ine her?

    content = forms.CharField(widget=forms.Textarea, label='Tekst')

    class Meta():
        model = Messages
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        self.content = kwargs.pop('content', None)
        super().__init__(*args, **kwargs)

    def getContent(self):
        """Returns content from user"""
        current_content = self.content
        return current_content

    def save(self, *args, **kwargs):
        """Creates the correct event-type and stores it in the database"""
        data = self.cleaned_data  #Gets the data from the form, stores it as a dict
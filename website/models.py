from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

"""Different models for the database, as well as methods to register entities"""

class rolleBrukerManager(BaseUserManager):
    """Adds a user to the database"""
    use_in_migrations = True

    def _create_user(self, username, email, password, is_superuser, is_bedrift, is_staff, rolleId, **extra_fields):
        """override"""
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        if email:
            email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        if is_superuser:
            user = self.model(username=username, email=email, is_active=True, is_bedrift=is_bedrift,
                              is_superuser=is_superuser,
                              is_staff=is_staff, last_login=now, date_joined=now, rolleId=1,)
        else:
            user = self.model(username=username, email=email, is_active=True, is_bedrift=is_bedrift, is_superuser=is_superuser,
                          is_staff=is_staff, last_login=now, date_joined=now, rolleId=rolleId, first_name=extra_fields.get('first_name'),
                          last_name=extra_fields.get('last_name'), bursdag=extra_fields.get('bursdag'),
                          strikkeNivaa=extra_fields.get('strikkeNivaa'))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_bedrift(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, True, False, 3,  **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, False, True, 1, **extra_fields)

    def create_user(self, username, email, password=None, **extra_fields):
        print("Creating user")
        return self._create_user(username, email, password, False, False, False, 2, **extra_fields)


class ArrangementManager(models.Manager):
    """Adds events to the database"""

    def __init__(self):
        super().__init__()

    use_in_migrations = True

    def _create_arrangement(self, type, title, innhold, forfatter, tidspunkt, location, **extra_fields):
        """override"""
        if not type:
            raise ValueError('Er dette ett arrangemant ett kurs eller en strikkekveld')
        arrangement = Arrangement(type=type, title=title, tidspunkt=tidspunkt, innhold=innhold, location=location, forfatter=forfatter)
        arrangement.save()
        return arrangement

    def create_kurs(self, title, innhold, forfatter, tidspunkt, location, **extra_fields):
        if forfatter.is_bedrift or forfatter.is_superuser:
            return self._create_arrangement('kurs', title, innhold, forfatter, tidspunkt, location, **extra_fields)
        else:
            return 'Du er ikke en bedrift og kan derfor ikke lage kurs!'

    def create_strikkeKveld(self, title, innhold, forfatter, tidspunkt, location, **extra_fields):
        if forfatter.is_bedrift:
            return 'Du er ikke en vanlig bruker og kan derfor ikke lage en strikkekveld!'
        return self._create_arrangement('strikkekveld', title, innhold, forfatter, tidspunkt, location, **extra_fields)

    def create_utfordring(self, title, innhold, forfatter, tidspunkt, location, **extra_fields):
        if forfatter.is_bedrift or forfatter.is_superuser:
            return self._create_arrangement('utfordring', title, innhold, forfatter, tidspunkt, location, **extra_fields)
        else:
            raise ValueError('Du er ikke en bedrift og kan derfor ikke lage kurs!')

class deltokArrangementManager(models.Manager):
    def participate(self, bruker, arrId):
        try:
            arr = Arrangement.objects.get(id=arrId)
        except:
            return False
        if len(deltokArrangement.objects.filter(arrangement=arr, bruker=bruker)) > 0:
            return False
        deltok = deltokArrangement(arrangement=arr, bruker=bruker)
        deltok.save()
        return deltok

    def unregister(self, bruker, arrId):
        try:
            arr = Arrangement.objects.get(id=arrId)
        except:
            return False
        return deltokArrangement.objects.filter(arrangement=arr, bruker=bruker).delete()



class Rolle(models.Model):

    rolleNavn = models.CharField(max_length=40)

    def __str__(self):
        return self.rolleNavn


class Bruker(AbstractUser):
    """Database table for User"""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('Brukernavn'),
        max_length=150,
        unique=True,
        help_text=_('Påkrevd. 150 tegn eller færre. Bare bokstaver, sifre og @ /. / + / - / _.'),
        validators=[username_validator],
        error_messages={
            'unique': _("Brukeren med dette brukernavn finnes allerede."),
        },
    )
    first_name = models.CharField(_('fornavn'), max_length=30, blank=True)
    last_name = models.CharField(_('etternavn'), max_length=150, blank=True)
    email = models.EmailField(_('epost'), blank=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    password = models.CharField(max_length=100)#will add hashing alg
    bursdag = models.DateTimeField(default=None, null=True)
    alder = models.IntegerField(null=True)
    rolleId = models.IntegerField()
    strikkeNivaa = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], null=True)
    objects = rolleBrukerManager()
    is_bedrift = models.BooleanField(_('bedrift status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        """Name used in the framework, for easier debugging"""
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_bruker_type(self):
        if self.is_superuser:
            return 'admin'
        elif self.is_bedrift:
            return 'bedrift'
        else:
            return 'vanlig_bruker'

class Arrangement(models.Model):
    """DB model for events"""

    type = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    tidspunkt = models.DateTimeField(default=timezone.now)
    innhold = models.TextField()
    location = models.CharField(max_length=50, null=True)
    forfatter = models.ForeignKey('Bruker', on_delete=models.CASCADE, null=True, default=None)

    objects = ArrangementManager()

    def __str__(self):
        return self.title + ' : ' + self.type

    class Meta:
        verbose_name = ('arrangement')
        verbose_name_plural = ('arrangementer')

    #add rolleId
    def get_strikeKvelder(self):
        strikkeKvelder = Arrangement.objects.filter(title='strikkekveld')
        return strikkeKvelder

    def get_kurs(self):
        kurs = Arrangement.objects.filter(title='kurs')
        return kurs

    def get_utfordringer(self):
        utfordringer = Arrangement.objects.filter(title='utfordring')
        return utfordringer

    def get_mineStrikeKvelder(self, bruker):
        strikkeKvelder = Arrangement.objects.filter(title='strikkekveld', forfatter=bruker)
        return strikkeKvelder

    def get_mineKurs(self, bruker):
        kurs = Arrangement.objects.filter(title='kurs', forfatter=bruker)
        return kurs

    def get_mineUtfordringer(self, bruker):
        utfordringer = Arrangement.objects.filter(title='utfordring', forfatter=bruker)
        return utfordringer

    def getMyArrangement(self, bruker):
        list_arrangementer = Arrangement.objects.filter(forfatter=bruker)
        return list_arrangementer


    def get_all(self):
        return Arrangement.objects.all()


class deltokArrangement(models.Model):
    arrangement = models.ForeignKey(Arrangement, on_delete=models.CASCADE, blank=True, null=True, default=None)
    bruker = models.ForeignKey(Bruker, on_delete=models.CASCADE, blank=True, null=True, default=None)

    objects = deltokArrangementManager()

    def getMyArrangementId(self, user):
        """ Get all the id-s of the registered events for this user"""
        list_id = []
        for arr in deltokArrangement.objects.all():
            if arr.bruker == user:
                list_id.append(arr.arrangement.id)
        return list_id




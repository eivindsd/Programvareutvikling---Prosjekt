from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractUser


class rolleBrukerManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, email, password, is_superuser, is_bedrift, is_staff, rolleId, **extra_fields):
        """override"""
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        #if not email or email == "" or email is None:
            #raise ValueError('The given email must be set')
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
    use_in_migrations = True
    def _create_arrangement(self, title, navn, innhold, forfatter, **extra_fields):
        """override"""
        now = timezone.now()
        if not title:
            raise ValueError('Er dette arrangemant et kurs eller en strikkekveld')
        arrangement = Arrangement(title=title, navn=navn, tidspunkt=now, innhold=innhold, forfatter=forfatter)
        arrangement.save()
        return arrangement

    def create_kurs(self, navn, innhold, forfatter, **extra_fields):
        if forfatter.is_bedrift:
            return self._create_arrangement(self, 'kurs', navn, innhold, forfatter, **extra_fields)
        else:
            return 'Du er ikke en bedrift og kan derfor ikke lage kurs!'

    def create_strikkeKveld(self, navn, innhold, forfatter, **extra_fields):
        if forfatter.is_bedrift and forfatter.is_superuser:
            return 'Du er ikke en vanlif bruker og kan derfor ikke lage en strikke kveld!'
        return self._create_arrangement(self, 'strikke kveld', navn, innhold, forfatter, **extra_fields)

    def create_utfordring(self, navn, innhold, forfatter, **extra_fields):
        if forfatter.is_bedrift:
            return self._create_arrangement(self, 'utfordring', navn, innhold, forfatter, **extra_fields)
        else:
            return 'Du er ikke en bedrift og kan derfor ikke lage kurs!'



class Rolle(models.Model):
    rolleNavn = models.CharField(max_length=40)

    def __str__(self):
        return self.rolleNavn


class Bruker(AbstractUser):
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
    strikkeNivaa = models.IntegerField(null=True)
    #is_staff = models.BooleanField(_('staff status'), default=True)
    objects = rolleBrukerManager()
    is_bedrift = models.BooleanField(_('bedrift status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)


    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

class Arrangement(models.Model):
    title = models.CharField(max_length=50)
    navn = models.CharField(max_length=50)
    tidspunkt = models.DateTimeField(default=timezone.now)
    innhold = models.TextField()
    forfatter = models.ForeignKey(Bruker, on_delete=models.CASCADE)

    objects = ArrangementManager()

    def __str__(self):
        return self.title + ' : ' + self.navn

    class Meta:
        verbose_name = ('arrangement')
        verbose_name_plural = ('arrangementer')

    #add rolleId
    def get_strikeKvelder(self):
        strikeKvelder = Arrangement.objects.filter(title='strikke kveld')
        return strikeKvelder

    def get_kurs(self):
        kurs = Arrangement.objects.filter(title='kurs')
        return kurs

    def get_utfordringer(self):
        utfordringer = Arrangement.objects.filter(title='utfordring')
        return utfordringer

    def get_mineStrikeKvelder(self, bruker):
        strikeKvelder = Arrangement.objects.filter(title='strikke kveld', forfatter=bruker)
        return strikeKvelder

    def get_mineKurs(self, bruker):
        kurs = Arrangement.objects.filter(title='kurs', forfatter=bruker)
        return kurs

    def get_mineUtfordringer(self, bruker):
        utfordringer = Arrangement.objects.filter(title='utfordring', forfatter=bruker)
        return utfordringer


class deltokArrangement(models.Model):
    arrangementId = models.ForeignKey(Arrangement, on_delete=models.CASCADE)
    brukerId = models.ForeignKey(Bruker, on_delete=models.CASCADE)


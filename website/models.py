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
    def _create_user(self, username, email, password, is_superuser, is_bedrift, is_staff, **extra_fields):
        """override"""
        now = timezone.now()
        print("I am here")
        if not username:
            raise ValueError('The given username must be set')
        if not email or email == "" or email is None:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, is_active=True, is_bedrift=is_bedrift, is_superuser=is_superuser,
                          is_staff=is_staff, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_bedrift(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, True, False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, False, True, **extra_fields)

    def create_user(self, username, email, password=None, **extra_fields):
        print("Creating user")
        return self._create_user(username, email, password, False, False, False, **extra_fields)


class Rolle(models.Model):
    rolleNavn = models.CharField(max_length=40)

    def __str__(self):
        return self.rolleNavn


class Bruker(AbstractUser):
    navn = models.CharField(max_length=50)
    #username = models.CharField(max_length=50,  unique=True)
    #email = models.EmailField(_('email address'), blank=True)
    password = models.CharField(max_length=100)#will add hashing alg
    bursdag = models.DateTimeField(default=None, null=True)
    alder = models.IntegerField(null=True)
    rolleId = models.ForeignKey(Rolle, on_delete=models.CASCADE, default=2)
    strikkeNivaa = models.IntegerField(null=True)
    #EMAIL_FIELD = 'email'
    #USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['email']
    #is_staff = models.BooleanField(_('staff status'), default=True)
    objects = rolleBrukerManager()
    is_bedrift = models.BooleanField(_('bedrift status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)


    def __str__(self):
        return self.navn

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

class Arrangement(models.Model):
    title = models.CharField(max_length=50)
    navn = models.CharField(max_length=50)
    tidspunkt = models.DateTimeField(default=timezone.now)
    innhold = models.TextField()
    forfatterId = models.ForeignKey(Bruker, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class deltokArrangement(models.Model):
    arrangementId = models.ForeignKey(Arrangement, on_delete=models.CASCADE)
    brukerId = models.ForeignKey(Bruker, on_delete=models.CASCADE)


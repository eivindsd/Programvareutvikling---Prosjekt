from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.contrib.auth.hashers import PBKDF2PasswordHasher

class Rolle(models.Model):
    rolleNavn = models.CharField(max_length=40)

    def __str__(self):
        return self.rolleNavn

class Bruker(models.Model):
    navn = models.CharField(max_length=50)
    brukerNavn = models.CharField(max_length=50)
    password = models.CharField(max_length=100)#will add hashing alg
    bursdag = models.DateTimeField(default=None, blank=True)
    alder = models.IntegerField()
    rolleId = models.ForeignKey(Rolle, on_delete=models.CASCADE)
    strikkeNivaa = models.IntegerField()

    def __str__(self):
        return self.navn

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


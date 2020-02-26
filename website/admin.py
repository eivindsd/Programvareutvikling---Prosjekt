from django.contrib import admin
from . import models

class brukerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'strikkeNivaa', 'rolleId', 'is_superuser')


admin.site.register(models.Bruker, brukerAdmin)


class arrangementAdmin(admin.ModelAdmin):
    list_display = ('title', 'tidspunkt', 'forfatterId')


admin.site.register(models.Arrangement, arrangementAdmin)

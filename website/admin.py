from django.contrib import admin
from . import models

"""Decides what fields will be displayed at the admin site, must match the name in website.models"""

class brukerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'strikkeNivaa', 'rolleId', 'is_superuser')


admin.site.register(models.Bruker, brukerAdmin)


class arrangementAdmin(admin.ModelAdmin):
    list_display = ('title', 'tidspunkt', 'forfatter')


admin.site.register(models.Arrangement, arrangementAdmin)

class deltokAdmin(admin.ModelAdmin):
    list_display = ('arrangement', 'bruker')


admin.site.register(models.deltokArrangement, deltokAdmin)

class innleggAdmin(admin.ModelAdmin):
    list_display = ('bruker', 'text')

admin.site.register(models.innlegg, innleggAdmin)

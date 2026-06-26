from django.contrib import admin
from medicos.models import Medico

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'crm', 'numero', 'email')
    list_filter = ('crm',)
    search_fields = ('nome', 'crm')
    ordering = ('nome',)

admin.site.register(Medico, MedicoAdmin)


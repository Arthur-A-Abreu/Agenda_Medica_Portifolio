from django.contrib import admin
from .models import Plantao

@admin.register(Plantao)
class PlantaoAdmin(admin.ModelAdmin):
    list_display = ('data', 'periodo', 'medico')
    list_filter = ('data', 'periodo', 'medico')
    search_fields = ('medico__nome', 'data')

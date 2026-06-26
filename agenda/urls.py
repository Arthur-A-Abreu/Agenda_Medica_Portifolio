from django.urls import path
from . import views

urlpatterns = [
    path('', views.agenda_medicos, name='agenda_medicos'),
    path('medico/<int:pk>/', views.agenda_detalhes, name='agenda_detalhes'),
    path('medico/<int:pk>/exportar/', views.exportar_agenda_excel, name='exportar_agenda_excel'),
    path('exportar_geral/', views.exportar_agenda_geral_excel, name='exportar_agenda_geral_excel'),
]

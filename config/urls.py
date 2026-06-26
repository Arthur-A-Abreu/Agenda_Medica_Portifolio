from django.urls import path
from . import views

urlpatterns = [
    path('', views.configuracoes_view, name='configuracoes'),
]

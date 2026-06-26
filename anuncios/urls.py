from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_anuncios, name='lista_anuncios'),
    path('criar/', views.criar_anuncio, name='criar_anuncio'),
    path('excluir/<int:pk>/', views.excluir_anuncio, name='excluir_anuncio'),
    path('status/<int:pk>/', views.alternar_status_anuncio, name='alternar_status_anuncio'),
]

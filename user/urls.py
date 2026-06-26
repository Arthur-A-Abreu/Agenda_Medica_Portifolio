from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('criar/', views.user_create, name='user_create'),
    path('<int:pk>/deletar/', views.user_delete, name='user_delete'),
    path('perfil/', views.profile_view, name='profile_view'),
    path('perfil/atualizar/', views.profile_update, name='profile_update'),
]

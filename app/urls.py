"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from medicos import views as medico_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('medicos/', medico_views.medico_list,   name='medico_list'),
    path('medicos/criar/', medico_views.medico_create, name='medico_create'),
    path('medicos/<int:pk>/editar/', medico_views.medico_edit,   name='medico_edit'),
    path('medicos/<int:pk>/apagar/', medico_views.medico_delete, name='medico_delete'),
    
    path('plantoes/', include('plantoes.urls')),
    path('dashboard/', include('deashboard.urls')),
    path('agenda/', include('agenda.urls')),
    path('configuracoes/', include('config.urls')),
    path('usuarios/', include('user.urls')),
    path('anuncios/', include('anuncios.urls')),
    path('', include('plantoes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

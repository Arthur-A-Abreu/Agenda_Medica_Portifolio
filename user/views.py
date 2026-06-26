from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from medicos.models import Medico

def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def user_list(request):
    """Lista todos os usuários do sistema."""
    users = User.objects.all().order_by('-is_superuser', 'username')
    medicos_sem_usuario = Medico.objects.filter(user__isnull=True)
    return render(request, 'user/user_list.html', {
        'users': users,
        'medicos_sem_usuario': medicos_sem_usuario
    })

@login_required
@user_passes_test(admin_only)
def user_create(request):
    """Cria um novo usuário e vincula a um médico se fornecido."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        medico_id = request.POST.get('medico_id')
        is_admin = request.POST.get('is_admin') == 'on'
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já existe.')
        else:
            user = User.objects.create_user(username=username, password=password)
            if is_admin:
                user.is_superuser = True
                user.is_staff = True
                user.save()
            
            if medico_id:
                medico = Medico.objects.get(id=medico_id)
                medico.user = user
                medico.save()
            
            messages.success(request, f'Usuário "{username}" criado com sucesso.')
    
    return redirect('user_list')

@login_required
@user_passes_test(admin_only)
def user_delete(request, pk):
    """Remove um usuário."""
    user = get_object_or_404(User, pk=pk)
    if user.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
        messages.error(request, 'Você não pode remover o único administrador.')
    else:
        username = user.username
        user.delete()
        messages.success(request, f'Usuário "{username}" removido.')
    return redirect('user_list')

@login_required
def profile_view(request):
    """Exibe o perfil do usuário logado."""
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def profile_update(request):
    """Atualiza dados do perfil (ex: senha)."""
    if request.method == 'POST':
        password = request.POST.get('password')
        password_conf = request.POST.get('password_conf')
        
        if password and password == password_conf:
            request.user.set_password(password)
            request.user.save()
            messages.success(request, 'Senha atualizada com sucesso. Por favor, faça login novamente.')
            return redirect('login')
        else:
            messages.error(request, 'As senhas não coincidem.')
            
    return redirect('profile_view')

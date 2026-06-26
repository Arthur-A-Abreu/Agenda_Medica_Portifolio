from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Medico

def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def medico_list(request):
    """Lista todos os médicos e processa o formulário de cadastro."""
    medicos = Medico.objects.all().order_by('nome')
    return render(request, 'medicos.html', {'medicos': medicos})


@login_required
@user_passes_test(admin_only)
def medico_create(request):
    """Cria um novo médico via POST e redireciona para a lista."""
    if request.method == 'POST':
        nome   = request.POST.get('nome', '').strip()
        crm    = request.POST.get('crm', '').strip()
        numero = request.POST.get('numero', '').strip()
        email  = request.POST.get('email', '').strip()
        foto   = request.FILES.get('foto')

        if nome and crm:
            Medico.objects.create(
                nome=nome,
                crm=crm,
                numero=numero or None,
                email=email or None,
                foto=foto,
            )
            messages.success(request, f'Médico "{nome}" cadastrado com sucesso!')
        else:
            messages.error(request, 'Nome e CRM são obrigatórios.')

    return redirect('medico_list')


@login_required
@user_passes_test(admin_only)
def medico_edit(request, pk):
    """Edita os dados de um médico existente via POST."""
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == 'POST':
        medico.nome   = request.POST.get('nome', medico.nome).strip()
        medico.crm    = request.POST.get('crm', medico.crm).strip()
        medico.numero = request.POST.get('numero', '').strip() or None
        medico.email  = request.POST.get('email', '').strip() or None

        nova_foto = request.FILES.get('foto')
        if nova_foto:
            medico.foto = nova_foto

        medico.save()
        messages.success(request, f'Médico "{medico.nome}" atualizado com sucesso!')

    return redirect('medico_list')


@login_required
@user_passes_test(admin_only)
def medico_delete(request, pk):
    """Apaga um médico via POST e redireciona para a lista."""
    medico = get_object_or_404(Medico, pk=pk)

    if request.method == 'POST':
        nome = medico.nome
        medico.delete()
        messages.success(request, f'Médico "{nome}" removido com sucesso!')

    return redirect('medico_list')




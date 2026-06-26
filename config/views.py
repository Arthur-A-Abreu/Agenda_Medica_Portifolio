from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Configuracao

def configuracoes_view(request):
    """Exibe e processa as configurações globais do sistema."""
    config, created = Configuracao.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        config.nome_hospital = request.POST.get('nome_hospital', config.nome_hospital)
        config.endereco = request.POST.get('endereco', config.endereco)
        config.horario_manha = request.POST.get('horario_manha', config.horario_manha)
        config.horario_tarde = request.POST.get('horario_tarde', config.horario_tarde)
        config.horario_noite = request.POST.get('horario_noite', config.horario_noite)
        config.notificacoes_email = 'notificacoes_email' in request.POST
        config.notificacoes_whatsapp = 'notificacoes_whatsapp' in request.POST
        
        if 'logo_hospital' in request.FILES:
            config.logo_hospital = request.FILES['logo_hospital']
            
        config.save()
        messages.success(request, 'Configurações atualizadas com sucesso!')
        return redirect('configuracoes')
        
    return render(request, 'configuracoes.html', {'config': config})

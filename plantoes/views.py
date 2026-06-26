from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
from medicos.models import Medico
from .models import Plantao, SolicitacaoTroca, HistoricoMudanca
from anuncios.models import Anuncio

MONTHS_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

@login_required
def calendario_view(request):
    today = date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if not (1 <= month <= 12):
            year, month = today.year, today.month
    except (ValueError, TypeError):
        year, month = today.year, today.month

    # Mes atual sendo visualizado
    current_month_name = f"{MONTHS_PT[month]} {year}"
    
    # Navegação: 4 antes e 4 depois do mês visualizado (9 no total, ativo sempre no centro)
    months_nav = []
    start_date = date(year, month, 1)
    for i in range(-4, 5):
        m_dt = start_date + relativedelta(months=i)
        months_nav.append({
            'year': m_dt.year,
            'month': m_dt.month,
            'name': f"{MONTHS_PT[m_dt.month][:3].upper()} {str(m_dt.year)[2:]}",
            'full_name': f"{MONTHS_PT[m_dt.month]} {m_dt.year}",
            'active': m_dt.year == year and m_dt.month == month
        })

    # Calendário
    cal = calendar.Calendar(firstweekday=6) # Domingo = 6
    month_days = cal.monthdayscalendar(year, month)
    
    # Plantões do mês
    shifts = Plantao.objects.filter(data__year=year, data__month=month).select_related('medico')
    
    # Organizar por dia e período para Template e JS
    shifts_by_day = {}
    shifts_json = {}
    for s in shifts:
        d = s.data.day
        # Para template
        if d not in shifts_by_day:
            shifts_by_day[d] = {}
        shifts_by_day[d][s.periodo] = s
        # Para JS
        if d not in shifts_json:
            shifts_json[d] = {}
        shifts_json[d][s.periodo] = {
            'id': s.id,
            'medico_id': s.medico.id,
            'medico_nome': s.medico.nome
        }

    # Médicos e contagem no mês visualizado
    medicos = Medico.objects.all().order_by('nome')
    doctor_stats = []
    for m in medicos:
        count = shifts.filter(medico=m).count()
        doctor_stats.append({
            'id': m.id,
            'nome': m.nome,
            'foto': m.foto.url if m.foto else None,
            'count': count
        })

    # Anúncios Ativos
    anuncios_ativos = Anuncio.objects.filter(
        ativo=True, 
        data_vencimento__gte=today
    ).order_by('-criado_em')

    # Lista de Plantões do Mês (Para a nova aba na sidebar)
    all_shifts_list = []
    for d_num in sorted(shifts_by_day.keys()):
        for p_code, p_obj in shifts_by_day[d_num].items():
            all_shifts_list.append({
                'dia': d_num,
                'periodo': p_obj.get_periodo_display(),
                'medico': p_obj.medico.nome,
                'periodo_code': p_code
            })

    context = {
        'year': year,
        'month': month,
        'current_month_name': current_month_name,
        'months_nav': months_nav,
        'month_days': month_days,
        'shifts_by_day': shifts_by_day,
        'shifts_json': shifts_json,
        'doctor_stats': doctor_stats,
        'medicos': medicos,
        'anuncios_ativos': anuncios_ativos,
        'all_shifts_list': all_shifts_list,
    }
    return render(request, 'calendario.html', context)

@csrf_exempt
@login_required
def atualizar_plantao(request):
    if request.method == 'POST':
        medico_id = request.POST.get('medico_id')
        data_str = request.POST.get('data')
        periodo = request.POST.get('periodo')
        
        # Validação de permissão: Apenas Admin ou o próprio Médico
        if not request.user.is_superuser:
            if not hasattr(request.user, 'perfil_medico') or str(medico_id) != str(request.user.perfil_medico.id):
                return JsonResponse({'status': 'error', 'message': 'Você só pode escalar a si mesmo.'})

        try:
            medico = Medico.objects.get(id=medico_id)
            plantao, created = Plantao.objects.update_or_create(
                data=data_str,
                periodo=periodo,
                defaults={'medico': medico}
            )
            return JsonResponse({
                'status': 'success', 
                'medico_nome': medico.nome,
                'created': created
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método inválido'})

@login_required
@csrf_exempt
def excluir_plantao(request):
    if request.method == 'POST':
        data_str = request.POST.get('data')
        periodo = request.POST.get('periodo')
        
        try:
            plantao = Plantao.objects.filter(data=data_str, periodo=periodo).first()
            if plantao and not request.user.is_superuser:
                if not hasattr(request.user, 'perfil_medico') or plantao.medico != request.user.perfil_medico:
                    return JsonResponse({'status': 'error', 'message': 'Você não tem permissão para remover este plantão.'})
            
            if plantao:
                plantao.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método inválido'})

@login_required
@csrf_exempt
def mudar_status_plantao(request):
    if request.method == 'POST':
        plantao_id = request.POST.get('plantao_id')
        novo_status = request.POST.get('status')
        try:
            plantao = Plantao.objects.get(id=plantao_id)
            
            # Validação de permissão
            if not request.user.is_superuser:
                if not hasattr(request.user, 'perfil_medico') or plantao.medico != request.user.perfil_medico:
                    return JsonResponse({'status': 'error', 'message': 'Você não tem permissão para alterar este status.'})

            plantao.status = novo_status
            plantao.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método inválido'})

@login_required
def solicitar_troca(request):
    if request.method == 'POST':
        plantao_id = request.POST.get('plantao_id')
        medico_novo_id = request.POST.get('medico_novo_id')
        mensagem = request.POST.get('mensagem', '')
        
        plantao = get_object_or_404(Plantao, id=plantao_id)
        medico_novo = get_object_or_404(Medico, id=medico_novo_id)
        
        # Verifica se o usuário tem um perfil médico associado
        if not hasattr(request.user, 'perfil_medico'):
            return JsonResponse({'status': 'error', 'message': 'Apenas médicos podem solicitar trocas.'})
            
        SolicitacaoTroca.objects.create(
            plantao=plantao,
            medico_solicitante=request.user.perfil_medico,
            medico_novo=medico_novo,
            mensagem=mensagem
        )
        return JsonResponse({'status': 'success', 'message': 'Solicitação enviada para aprovação do Admin.'})
    return JsonResponse({'status': 'error', 'message': 'Método inválido.'})

@login_required
def gerenciar_trocas(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    solicitacoes = SolicitacaoTroca.objects.filter(status='P').order_by('-criado_em')
    return render(request, 'plantoes/gerenciar_trocas.html', {'solicitacoes': solicitacoes})

@login_required
@csrf_exempt
def responder_troca(request, troca_id):
    if not request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Acesso negado.'})
        
    acao = request.POST.get('acao') # 'aprovar' ou 'recusar'
    troca = get_object_or_404(SolicitacaoTroca, id=troca_id)
    
    if acao == 'aprovar':
        plantao = troca.plantao
        medico_antigo = plantao.medico
        medico_novo = troca.medico_novo
        
        # Executa a troca
        plantao.medico = medico_novo
        plantao.save()
        
        troca.status = 'A'
        troca.respondido_em = timezone.now()
        troca.save()
        
        # Registra no Histórico
        HistoricoMudanca.objects.create(
            descricao=f"Troca aprovada: {medico_antigo.nome} -> {medico_novo.nome} no dia {plantao.data.strftime('%d/%m/%Y')}",
            autor=request.user
        )
        
        return JsonResponse({'status': 'success', 'message': 'Troca aprovada com sucesso!'})
        
    elif acao == 'recusar':
        troca.status = 'R'
        troca.respondido_em = timezone.now()
        troca.save()
        return JsonResponse({'status': 'success', 'message': 'Troca recusada.'})
        
    return JsonResponse({'status': 'error', 'message': 'Ação inválida.'})

@login_required
def historico_mudancas(request):
    historico = HistoricoMudanca.objects.all().order_by('-data_mudanca')
    return render(request, 'plantoes/historico.html', {'historico': historico})
@login_required
@csrf_exempt
def replicar_plantao_mes(request):
    """Replica o plantão selecionado para todos os mesmos dias da semana no mês corrente."""
    if request.method == 'POST':
        medico_id = request.POST.get('medico_id')
        data_origem_str = request.POST.get('data')
        periodo = request.POST.get('periodo')
        
        if not medico_id or not data_origem_str or not periodo:
            return JsonResponse({'status': 'error', 'message': 'Dados incompletos.'})

        if not request.user.is_superuser:
            return JsonResponse({'status': 'error', 'message': 'Apenas administradores podem replicar escalas.'})

        try:
            medico = Medico.objects.get(id=medico_id)
            data_origem = date.fromisoformat(data_origem_str)
            weekday = data_origem.weekday() # 0 = Segunda, 6 = Domingo
            
            # Encontrar todos os dias do mesmo mês e ano
            year, month = data_origem.year, data_origem.month
            _, num_days = calendar.monthrange(year, month)
            
            count = 0
            # Iterar do dia seguinte até o fim do mês
            for day in range(data_origem.day + 1, num_days + 1):
                current_date = date(year, month, day)
                if current_date.weekday() == weekday:
                    Plantao.objects.update_or_create(
                        data=current_date,
                        periodo=periodo,
                        defaults={'medico': medico}
                    )
                    count += 1
            
            return JsonResponse({
                'status': 'success', 
                'message': f'Plantão replicado para mais {count} dias com sucesso!'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método inválido'})

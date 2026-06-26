from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from datetime import date
import calendar
from plantoes.models import Plantao
from medicos.models import Medico

MONTHS_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

@login_required
def dashboard_view(request):
    today = date.today()
    year = today.year
    month = today.month
    
    # Total de slots no mês (Dias * 4 - agora incluindo o slot de Dia)
    _, num_days = calendar.monthrange(year, month)
    total_slots = num_days * 4
    
    # Plantões realizados no mês selecionado (atual)
    shifts = Plantao.objects.filter(data__year=year, data__month=month)
    filled_slots = shifts.count()
    missing_slots = total_slots - filled_slots
    
    # Top 5 Médicos (mais plantões no mês)
    top_medicos = Medico.objects.annotate(
        num_plantoes=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month))
    ).order_by('-num_plantoes')[:5]
    
    # Bottom 5 Médicos (menos plantões no mês)
    bottom_medicos = Medico.objects.annotate(
        num_plantoes=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month))
    ).order_by('num_plantoes')[:5]

    # Lista Completa de Médicos com Breakdown por Período (Este Mês)
    medicos_stats = Medico.objects.annotate(
        count_dia=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month, plantoes__periodo='D')),
        count_manha=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month, plantoes__periodo='M')),
        count_tarde=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month, plantoes__periodo='T')),
        count_noite=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month, plantoes__periodo='N')),
        total=Count('plantoes', filter=Q(plantoes__data__year=year, plantoes__data__month=month))
    ).order_by('nome')
    
    context = {
        'month_name': MONTHS_PT[month],
        'year': year,
        'total_slots': total_slots,
        'filled_slots': filled_slots,
        'missing_slots': missing_slots,
        'filled_percent': round((filled_slots / total_slots) * 100, 1) if total_slots > 0 else 0,
        'top_medicos': top_medicos,
        'bottom_medicos': bottom_medicos,
        'medicos_stats': medicos_stats,
    }
    return render(request, 'dashboard.html', context)

from .models import Configuracao
from plantoes.models import SolicitacaoTroca

def global_settings(request):
    """Disponibiliza as configurações globais em todos os templates."""
    config, _ = Configuracao.objects.get_or_create(id=1)
    
    pending_swaps = 0
    if request.user.is_authenticated and request.user.is_superuser:
        pending_swaps = SolicitacaoTroca.objects.filter(status='P').count()
        
    return {
        'global_config': config,
        'pending_swaps_count': pending_swaps
    }

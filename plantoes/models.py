from django.db import models
from medicos.models import Medico

class Plantao(models.Model):
    PERIODOS = (
        ('D', 'Dia (07:00-19:00)'),
        ('M', 'Manhã (07:00-13:00)'),
        ('T', 'Tarde (13:00-19:00)'),
        ('N', 'Noite (19:00-07:00)'),
    )
    
    STATUS_CHOICES = (
        ('P', 'Agendado'),
        ('C', 'Concluído'),
        ('F', 'Faltou'),
    )
    
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='plantoes')
    data = models.DateField()
    periodo = models.CharField(max_length=1, choices=PERIODOS)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        verbose_name = 'Plantão'
        verbose_name_plural = 'Plantões'
        unique_together = ('data', 'periodo')

    def __str__(self):
        return f"{self.data} - {self.get_periodo_display()} - {self.medico.nome}"

class SolicitacaoTroca(models.Model):
    STATUS_TROCA = (
        ('P', 'Pendente'),
        ('A', 'Aprovado'),
        ('R', 'Recusado'),
    )
    
    plantao = models.ForeignKey(Plantao, on_delete=models.CASCADE, related_name='solicitacoes')
    medico_solicitante = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='solicitacoes_enviadas')
    medico_novo = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='solicitacoes_recebidas')
    status = models.CharField(max_length=1, choices=STATUS_TROCA, default='P')
    criado_em = models.DateTimeField(auto_now_add=True)
    respondido_em = models.DateTimeField(null=True, blank=True)
    mensagem = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Troca: {self.medico_solicitante} -> {self.medico_novo} ({self.plantao.data})"

class HistoricoMudanca(models.Model):
    data_mudanca = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    autor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.data_mudanca.strftime('%d/%m/%Y')} - {self.descricao[:50]}"

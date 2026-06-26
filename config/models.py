from django.db import models

class Configuracao(models.Model):
    # Hospital
    nome_hospital = models.CharField(max_length=200, default='MedAgenda Hospital')
    logo_hospital = models.ImageField(upload_to='logos/', blank=True, null=True)
    endereco = models.CharField(max_length=300, blank=True, null=True)
    
    # Horários de Turnos
    horario_manha = models.CharField(max_length=5, default='07:00')
    horario_tarde = models.CharField(max_length=5, default='13:00')
    horario_noite = models.CharField(max_length=5, default='19:00')
    
    # Notificações
    notificacoes_email = models.BooleanField(default=True)
    notificacoes_whatsapp = models.BooleanField(default=False)
    
    def __str__(self):
        return "Configurações Gerais"

    class Meta:
        verbose_name = "Configuração"
        verbose_name_plural = "Configurações"

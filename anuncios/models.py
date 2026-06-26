from django.db import models
from django.contrib.auth.models import User

class Anuncio(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor (Admin)")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Anúncio"
        verbose_name_plural = "Anúncios"
        ordering = ['-criado_em']

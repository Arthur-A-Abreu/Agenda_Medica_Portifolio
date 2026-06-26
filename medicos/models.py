from django.db import models
from django.contrib.auth.models import User

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='perfil_medico')
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20)
    numero = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_medicos/', blank=True, null=True)
    
    def __str__(self):
        return self.nome

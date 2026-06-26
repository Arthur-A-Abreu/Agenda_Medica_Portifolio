from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Anuncio
from django.utils import timezone

@login_required
@staff_member_required
def lista_anuncios(request):
    anuncios = Anuncio.objects.all().order_by('-criado_em')
    return render(request, 'anuncios/lista.html', {'anuncios': anuncios})

@login_required
@staff_member_required
def criar_anuncio(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        conteudo = request.POST.get('conteudo')
        data_vencimento = request.POST.get('data_vencimento')
        
        Anuncio.objects.create(
            titulo=titulo,
            conteudo=conteudo,
            autor=request.user,
            data_vencimento=data_vencimento
        )
        return redirect('lista_anuncios')
    return render(request, 'anuncios/criar.html')

@login_required
@staff_member_required
def excluir_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    anuncio.delete()
    return redirect('lista_anuncios')

@login_required
@staff_member_required
def alternar_status_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    anuncio.ativo = not anuncio.ativo
    anuncio.save()
    return redirect('lista_anuncios')

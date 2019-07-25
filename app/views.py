from django.shortcuts import render, redirect
from app.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404
from django.views.decorators.http import require_POST

# Create your views here.
@login_required(login_url='/login/')
def listaEvento(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario).order_by('data_evento')
    # eventos = Evento.objects.filter(usuario=usuario)
    dados = {}
    dados['eventos'] =  eventos
    dados['usuario'] = usuario
    return render(request, 'agenda/agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    idEvento = request.GET.get('id')
    dados = {}
    if idEvento:
        dados['evento'] = Evento.objects.get(id=idEvento)
    dados['usuario'] = request.user
    return render(request, 'agenda/evento.html', dados)

def verificaData(data_evento):
    dataAtual = datetime.now()
    data_evento = data_evento.replace('T', ' ')
    data_evento_time = datetime.strptime(data_evento, '%Y-%m-%d %H:%M')
    print(data_evento)
    print(dataAtual)
    if data_evento_time>dataAtual: d = True
    else: d = False
    return d

@login_required(login_url='/login/')
@require_POST
def submit_evento(request):
    idEvento = request.POST.get('id')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    data_evento = request.POST.get('data_evento')
    usuario = request.user
    d = verificaData(data_evento)
    if d == False and not idEvento:
        messages.error(request, "Insira uma data futura")
        return redirect('/agenda/evento/')
    elif d == False and idEvento:
        messages.error(request, "Insira uma data futura")
    elif idEvento and d == True:
        evento = Evento.objects.get(id=idEvento)
        if evento.usuario == usuario:
            evento.titulo = titulo
            evento.descricao = descricao
            evento.data_evento = data_evento
            evento.save()
            messages.success(request, 'Alteração com sucesso')
    elif not idEvento and d == True:
        Evento.objects.create(titulo=titulo, descricao=descricao, data_evento=data_evento, usuario=usuario)
        messages.success(request, 'Criado com sucesso')
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id)
    except Exception:
        raise Http404()
    if evento.usuario == usuario:
        evento.delete()
        messages.success(request, 'Deletado com sucesso')
    else:
        raise Http404()
    return redirect('/')


from django.shortcuts import render, redirect
from app.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime,timedelta
from django.http.response import Http404

# Create your views here.
@login_required(login_url='/login/')
def listaEvento(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario).order_by('data_evento')
    # eventos = Evento.objects.filter(usuario=usuario)
    dados = {'eventos' :  eventos}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    idEvento = request.GET.get('id')
    dados = {}
    if idEvento:
        dados['evento'] = Evento.objects.get(id=idEvento)
    return render(request, 'evento.html', dados)

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
def submit_evento(request):
    if request.POST:
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
    else:
        raise Http404()
    return redirect('/')

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
        else:
            messages.error(request, "Usuário e/ou SEnha Inválido(s)")
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

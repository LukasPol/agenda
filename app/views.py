from django.shortcuts import render, redirect
from app.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

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

@login_required(login_url='/login/')
def listaEvento(request):
    usuario = request.user
    eventos = Evento.objects.filter(usuario=usuario)
    dados = {'eventos' :  eventos}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    idEvento = request.GET.get('id')
    dados = {}
    if idEvento:
        dados['evento'] = Evento.objects.get(id=idEvento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        idEvento = request.POST.get('id')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data_evento')
        usuario = request.user
        if idEvento:
            evento = Evento.objects.get(id=idEvento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()
            # Evento.objects.filter(id=idEvento).update(titulo=titulo, descricao=descricao, data_evento=data_evento) 
        else:
            Evento.objects.create(titulo=titulo, descricao=descricao, data_evento=data_evento, usuario=usuario)

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id):
    usuario = request.user
    evento = Evento.objects.get(id=id)
    if evento.usuario == usuario:
        evento.delete()
    return redirect('/')
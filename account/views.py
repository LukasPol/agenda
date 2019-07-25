from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def login_user(request):
    return render(request, 'account/login.html')

@require_POST
def submit_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    usuario = authenticate(username=username, password=password)
    if usuario is not None:
        login(request, usuario)
    else:
        messages.error(request, "Usuário e/ou Senha Inválido(s)")
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

def register(request):
    return render(request, 'account/register.html')

@require_POST
def submit_register(request):
    try:
        usuario_name = User.objects.get(username=request.POST.get('username'))
        usuario_email = User.objects.get(email=request.POST.get('email'))

        if usuario_name or usuario_email:
            messages.error(request, "Usuário e/ou Email está sendo usado")
        return redirect('/register/')
    except:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        novoUser = User.objects.create_user(username=username,email=email, password=password)
        novoUser.save()
        return redirect('/')
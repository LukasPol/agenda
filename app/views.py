from django.shortcuts import render, HttpResponse
from .models import Evento
# from models import Evento

# Create your views here.
def evento(request, tituloEvento):
    # Evento.
    # Evento.objects.get(titulo = tituloEvento)
    return HttpResponse()

def listaEvento(request):
    evento = Evento.objects.get(id=1)
    response = {'evento' :  evento}
    return render(request, 'agenda.html', response)

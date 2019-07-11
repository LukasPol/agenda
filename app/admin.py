from django.contrib import admin
from app.models import Evento

# Mostrar determinados campos
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'data_criacao')
    list_filter = ('usuario',)

# Register your models here.
admin.site.register(Evento, EventoAdmin)
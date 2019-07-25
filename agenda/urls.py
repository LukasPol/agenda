"""agenda URL Configuration
The `urlpatterns` list routes URLs to . For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function 
    1. Add an import:  from my_app import 
    2. Add a URL to urlpatterns:  path('', .home, name='home')
Class-based 
    1. Add an import:  from other_app. import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import listaEvento, evento, delete_evento, submit_evento
from account.views import login_user, submit_login, logout_user, register, submit_register
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agenda/', listaEvento),
    path('', RedirectView.as_view(url='/agenda/')),
    path('agenda/evento/', evento),
    path('agenda/evento/submit', submit_evento),
    path('agenda/evento/delete/<int:id>/', delete_evento),
    path('login/', login_user),
    path('login/submit', submit_login),
    path('logout/', logout_user),
    path('register/', register ),
    path('register/submit', submit_register )
]
"""
URL configuration for consultorio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import (AgendarCitaView, CancelarReprogramarCitaView,
                    DisponibilidadHorariosView, PacienteListCreateView,
                    index_view)

# Aquí cargamos las URLs que vayamos a usar para las pruebas.
urlpatterns = [
    path('', index_view, name='opciones'),  # Página principal con las opciones a elegir.
    path('admin/', admin.site.urls),
    path('citas/paciente/', PacienteListCreateView.as_view(), name='gestionar_paciente'),
    path('citas/agendar/', AgendarCitaView.as_view(), name='agendar_cita'),
    path('citas/disponibilidad/', DisponibilidadHorariosView.as_view(), name='disponibilidad_horarios'),
    path('citas/gestionarcita/', CancelarReprogramarCitaView.as_view(), name='cancelar_reprogramar_cita'),
]
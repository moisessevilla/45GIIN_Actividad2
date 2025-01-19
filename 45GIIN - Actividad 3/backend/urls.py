from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CitaViewSet, MedicoViewSet, PacienteViewSet, index_view

router = DefaultRouter()
router.register(r'paciente', PacienteViewSet, basename='paciente')
router.register(r'medico', MedicoViewSet, basename='medico')
router.register(r'cita', CitaViewSet, basename='cita')

# Aquí cargamos las URLs que vayamos a usar para las pruebas.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', index_view, name='opciones'),  # Página principal con las opciones a elegir.
]

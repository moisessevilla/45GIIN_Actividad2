from django.db import transaction
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import Cita, Medico, Paciente
from .serializers import CitaSerializer, MedicoSerializer, PacienteSerializer


# Vista principal
def index_view(request):

    # Renderiza la página principal con las opciones a elegir.
    try:
        return render(request, "opciones.html")
    except Exception as e:
        return Response(
            {"error": f"Error al cargar la página: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Habilitar Logs en el Backend
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Si ya existe una respuesta, se devuelve en JSON
        response.data["status_code"] = response.status_code
    else:
        # Si es un error no controlado, se devuelve este mensaje
        return Response(
            {"error": "Se ha producido un error inesperado.", "detalle": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response


# CRUD Paciente
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all().order_by("id_paciente")
    serializer_class = PacienteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Paciente eliminado exitosamente."}, status=status.HTTP_200_OK
        )


# CRUD Medico
class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all().order_by("id_medico")
    serializer_class = MedicoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Medico eliminado exitosamente."}, status=status.HTTP_200_OK
        )


# CRUD Cita
class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all().order_by("id_cita")
    serializer_class = CitaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"Mensaje": "Cita eliminada exitosamente."}, status=status.HTTP_200_OK
        )


@api_view(["GET"])
def obtener_cita(request):
    id_cita = request.query_params.get("id_cita", None)
    if id_cita:
        try:
            cita = Cita.objects.get(id_cita=id_cita)
            serializer = CitaSerializer(cita)
            return Response(serializer.data)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada."}, status=404)
    return Response({"error": "ID de cita no proporcionado."}, status=400)

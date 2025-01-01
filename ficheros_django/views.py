from django.db import transaction
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cita, Medico, Paciente
from .serializers import CitaSerializer, MedicoSerializer, PacienteSerializer


# Vista principal
def index_view(request):
    
    # Renderiza la página principal con las opciones a elegir.
    try:
        return render(request, 'opciones.html')
    except Exception as e:
        return Response({"error": f"Error al cargar la página: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Permite listar y crear instancias de Paciente.
class PacienteListCreateView(ListCreateAPIView):

    # GET: Lista todos los pacientes.
    # POST: Crea uno o varios pacientes.

    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def create(self, request, *args, **kwargs):
        
        # Sobrescribe el método create para permitir creación masiva de pacientes.
        data = request.data
        if isinstance(data, list):  # Múltiples JSON
            with transaction.atomic():
                errores = []
                resultados = []
                for paciente_data in data:
                    serializer = self.get_serializer(data=paciente_data)
                    if serializer.is_valid():
                        serializer.save()
                        resultados.append(serializer.data)
                    else:
                        errores.append({"error": serializer.errors})
                return Response({"resultados": resultados, "errores": errores}, status=status.HTTP_207_MULTI_STATUS)
        return super().create(request, *args, **kwargs)


class PacienteRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
    # Permite obtener, actualizar o eliminar instancias de Paciente por su ID.
    # - GET: Recupera un paciente.
    # - PUT/PATCH: Actualiza un paciente.
    # - DELETE: Elimina un paciente.
    
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

# Maneja la creación de citas médicas.
class AgendarCitaView(APIView):

    # GET: Devuelve un mensaje indicando que solo acepta POST.
    def get(self, request):
        return Response({
            "mensaje": "Este endpoint es solo para agendar citas. Use el método POST con los datos necesarios."
        }, status=200)

    # POST: Crea una nueva cita médica.
    def post(self, request):
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                id_paciente = serializer.validated_data['id_paciente']
                id_medico = serializer.validated_data['id_medico']
                fecha = serializer.validated_data['fecha']
                hora = serializer.validated_data['hora']

                # Validación de existencia de paciente y médico
                if not Paciente.objects.filter(id_paciente=id_paciente.id_paciente).exists():
                    return Response({"error": "El paciente no existe."}, status=status.HTTP_404_NOT_FOUND)

                if not Medico.objects.filter(id_medico=id_medico.id_medico).exists():
                    return Response({"error": "El médico no existe."}, status=status.HTTP_404_NOT_FOUND)

                # Validación de citas duplicadas
                if Cita.objects.filter(id_paciente=id_paciente, id_medico=id_medico, fecha=fecha, hora=hora).exists():
                    return Response({"error": "Ya existe una cita en este horario."}, status=status.HTTP_400_BAD_REQUEST)

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Consulta la disponibilidad de horarios para una especialidad y fecha específicas.
class DisponibilidadHorariosView(APIView):

    # GET: Devuelve los horarios disponibles.
    def get(self, request):
        especialidad = request.query_params.get('especialidad')
        fecha = request.query_params.get('fecha')

        # Validación de parámetros
        if not especialidad:
            return Response({"error": "El parámetro 'especialidad' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        if not fecha:
            return Response({"error": "El parámetro 'fecha' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ocupados = Cita.objects.filter(id_medico__especialidad=especialidad, fecha=fecha).values_list('hora', flat=True)
            horarios_ocupados = [hora.strftime("%H:%M:%S") for hora in ocupados]

            horarios_totales = ["09:00:00", "10:00:00", "11:00:00", "13:00:00", "14:00:00", "15:00:00"]
            disponibles = [h for h in horarios_totales if h not in horarios_ocupados]

            return Response({"disponibles": disponibles}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al consultar disponibilidad: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Permite consultar, reprogramar o cancelar citas médicas.
class CancelarReprogramarCitaView(APIView):

    # GET: Consulta citas por parámetros.
    def get(self, request):
        id_cita = request.query_params.get('id_cita')
        id_paciente = request.query_params.get('id_paciente')
        id_medico = request.query_params.get('id_medico')

        # Validación de parámetros
        if not (id_cita or id_paciente or id_medico):
            return Response({"error": "Debe proporcionar al menos un parámetro (id_cita, id_paciente o id_medico)."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            citas = Cita.objects.all()
            if id_cita:
                citas = citas.filter(id_cita=id_cita)
            if id_paciente:
                citas = citas.filter(id_paciente=id_paciente)
            if id_medico:
                citas = citas.filter(id_medico=id_medico)

            serializer = CitaSerializer(citas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al consultar citas: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH: Reprograma una cita.
    def patch(self, request):
        id_cita = request.data.get('id_cita')
        if not id_cita:
            return Response({"error": "Debe proporcionar id_cita."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cita = Cita.objects.get(id_cita=id_cita)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        nueva_fecha = request.data.get('fecha')
        nueva_hora = request.data.get('hora')

        if not nueva_fecha or not nueva_hora:
            return Response({"error": "Debe proporcionar tanto la fecha como la hora para reprogramar."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                if (cita.fecha == nueva_fecha and cita.hora == nueva_hora):
                    return Response({"error": "El nuevo horario es el mismo que el actual."}, status=status.HTTP_400_BAD_REQUEST)
                if Cita.objects.filter(fecha=nueva_fecha, hora=nueva_hora).exclude(id_cita=id_cita).exists():
                    return Response({"error": "El nuevo horario ya está ocupado."}, status=status.HTTP_400_BAD_REQUEST)
                cita.fecha = nueva_fecha
                cita.hora = nueva_hora
                cita.save()
                return Response({"mensaje": "Cita reprogramada exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al reprogramar cita: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE: Cancela una cita.
    def delete(self, request):
        id_cita = request.query_params.get('id_cita')
        if not id_cita:
            return Response({"error": "Debe proporcionar id_cita."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cita = Cita.objects.get(id_cita=id_cita)
            cita.delete()
            return Response({"mensaje": "Cita cancelada exitosamente."}, status=status.HTTP_200_OK)
        except Cita.DoesNotExist:
            return Response({"error": "Cita no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error al cancelar cita: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

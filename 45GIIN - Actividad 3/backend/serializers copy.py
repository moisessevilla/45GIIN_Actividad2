from rest_framework import serializers

from .models import Cita, Medico, Paciente


# Serializer para el modelo Paciente
class PacienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Paciente.
    Convierte instancias de Paciente en datos JSON y viceversa.
    """
    class Meta:
        model = Paciente  # Modelo asociado al serializer
        fields = '__all__'  # Incluye todos los campos del modelo


# Serializer para el modelo Medico
class MedicoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Medico.
    Convierte instancias de Medico en datos JSON y viceversa.
    """
    class Meta:
        model = Medico  # Modelo asociado al serializer
        fields = '__all__'  # Incluye todos los campos del modelo


# Serializer para el modelo Cita
class CitaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cita.
    Incluye validaciones personalizadas para los campos `fecha` y `hora`.
    """
    class Meta:
        model = Cita  # Modelo asociado al serializer
        fields = '__all__'  # Incluye todos los campos del modelo
        """read_only_fields = ['id_cita']  # El campo `id_cita` es de solo lectura"""

    # Representa las relaciones ForeignKey con información detallada
    id_paciente = PacienteSerializer(read_only=True)  # Serializa el objeto completo del paciente
    id_paciente_id = serializers.PrimaryKeyRelatedField(
        source='id_paciente', queryset=Paciente.objects.all(), write_only=True
    )  # Para recibir solo el ID al crear o actualizar

    id_medico = MedicoSerializer(read_only=True)  # Serializa el objeto completo del médico
    id_medico_id = serializers.PrimaryKeyRelatedField(
        source='id_medico', queryset=Medico.objects.all(), write_only=True
    )  # Para recibir solo el ID al crear o actualizar

    def validate_fecha(self, value):
        """
        Validación personalizada para el campo `fecha`.
        Se asegura de que la fecha no sea anterior a la fecha actual.
        """
        from datetime import date
        if value < date.today():  # Verifica si la fecha es pasada
            raise serializers.ValidationError("La fecha no puede ser en el pasado.")
        return value  # Retorna la fecha si es válida

    def validate_hora(self, value):
        """
        Validación personalizada para el campo `hora`.
        Se asegura de que la hora esté dentro del horario laboral (9:00 a 17:00).
        """
        import datetime

        # Verifica si la hora está fuera del rango permitido
        if value < datetime.time(9, 0) or value > datetime.time(17, 0):
            raise serializers.ValidationError("La hora debe estar entre las 09:00 y las 17:00.")
        return value  # Retorna la hora si es válida

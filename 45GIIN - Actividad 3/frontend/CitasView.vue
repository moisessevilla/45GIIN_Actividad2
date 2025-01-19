<template>
  <div class="contenido">
    <h1>Consulta de Citas</h1>

    <!-- Contenedor de citas -->
    <div class="citas-contenedor">
      <div v-if="cita" class="detalle-cita">
        <h2>Detalles de la Cita</h2>
        <p><strong>ID Cita:</strong> {{ cita.id_cita }}</p>
        <p><strong>Referencia Cita:</strong> {{ cita.refcita }}</p>
        <p><strong>DNI:</strong> {{ cita.paciente_dni }}</p>
        <p><strong>Paciente:</strong> {{ cita.paciente_nombre }} ({{ cita.paciente_apellido }})</p>
        <p><strong>Especialidad:</strong> {{ cita.medico_especialidad }}</p>
        <p><strong>Médico:</strong> {{ cita.medico_nombre }}</p>
        <p><strong>Fecha:</strong> {{ cita.fecha }}</p>
        <p><strong>Hora:</strong> {{ cita.hora }}</p>
        <p><strong>Estado:</strong> {{ cita.estado }}</p>
      </div>
    </div>

    <!-- Mensaje en caso de no encontrar la cita -->
    <div v-if="loading" class="loading">
      <p>Cargando...</p>
    </div>
    <div v-else-if="!loading && searchId && !cita" class="no-cita">
      <p>No tienes ninguna cita agendada.</p>
    </div>

    <!-- Mensaje de error -->
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchId: null, // ID de la cita a buscar
      cita: null, // Datos de la cita obtenida
      loading: false, // Indicador de carga
      error: null, // Mensaje de error
    };
  },
  methods: {
    async fetchCitaById() {
      // Restablecer valores previos
      this.cita = null;
      this.error = null;
      this.loading = true;

      try {
        const response = await axios.get(`/cita/?id_paciente=${this.searchId}`);
        const data = response.data;

        // Reorganizar los datos para adaptarlos al frontend
        this.cita = {
          id_cita: data.id_cita,
          refcita : data.refcita,
          paciente_dni: data.id_paciente.dni,
          paciente_nombre: `${data.id_paciente.nombre} ${data.id_paciente.apellido}`,
          medico_especialidad: data.id_medico.especialidad,
          medico_nombre: data.id_medico.nombre,
          fecha: data.fecha,
          hora: data.hora,
          estado: data.estado || "Desconocido",
        };
      } catch (err) {
        console.error("Error al buscar la cita:", err);
        this.error = "Error al buscar la cita. Intente nuevamente.";
      } finally {
        this.loading = false; // Finalizar carga
      }
    },
  },
};
</script>

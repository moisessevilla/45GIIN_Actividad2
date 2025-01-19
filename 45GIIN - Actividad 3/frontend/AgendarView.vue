<template>
  <div class="contenido">
    <h1>Gestión de Citas Médicas</h1>

    <!-- Formulario para crear/editar citas -->
    <form @submit.prevent="handleSubmit" class="formulario">
      <!-- Paciente -->
      <div class="form-group">
        <label for="id_paciente">Paciente:*</label>
        <!-- Mostrar select en modo creación, input en modo edición -->
        <select id="id_paciente" v-model="form.id_paciente" required>
          <option value="" disabled>Seleccione un paciente</option>
          <option v-for="paciente in pacientes" :key="paciente.id_paciente" :value="paciente.id_paciente">
            {{ paciente.nombre }} {{ paciente.apellido }}
          </option>
        </select>
      </div>

      <!-- Médico/Especialidad -->
      <div class="form-group">
        <label for="id_medico">Especialidad:*</label>
        <!-- Mostrar select en modo creación, input en modo edición -->
        <select id="id_medico" v-model="form.id_medico" required>
          <option value="" disabled>Seleccione una Especialidad</option>
          <option v-for="medico in medicos" :key="medico.id_medico" :value="medico.id_medico">
            {{ medico.especialidad }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="fecha">Fecha:*</label>
        <input id="fecha" type="date" v-model="form.fecha" @change="formatFecha" />
      </div>
      <div class="form-group">
        <label for="hora">Hora:*</label>
        <input id="hora" v-model="form.hora" type="time" required />
      </div>
      <!-- ✅ Estado de la cita -->
      <div class="form-group">
        <label for="estado">Confirmar Cita:</label>
        <input type="checkbox" id="estado" v-model="form.estado" />
      </div>
      <div class="form-group">
        <label for="cita_auto">Cita automática:</label>
        <input type="checkbox" id="cita_auto" v-model="form.cita_auto" />
      </div>
      <div class="form-group3">
        <label for="refcita">Referencia Cita:</label>
        <span style="margin-left: 22px;" id="refcita">{{ form.refcita || 'Se generará automáticamente' }}</span>
      </div>
      <div class="info">
        <label for="info">* Campos requeridos.</label>
      </div>
      <div class="form-buttons">
        <button type="submit">{{ form.id_cita ? 'Actualizar' : 'Crear' }} Cita</button>
        <button type="button" v-if="form.id_cita" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <select v-model="searchKey" class="busqueda-select">
        <option value="id_cita">ID Cita</option>
        <option value="refcita">Ref. Cita</option>
        <option value="paciente">Paciente</option>
        <option value="especialidad">Especialidad</option>
        <option value="medico">Médico</option>
        <option value="estado">Estado</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>

    <!-- Tabla de citas -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th @click="sortTable('id_cita')">ID Cita</th>
            <th @click="sortTable('refcita')">Ref. Cita</th>
            <th @click="sortTable('paciente')">Paciente</th>
            <th @click="sortTable('especialidad')">Especialidad</th>
            <th @click="sortTable('medico')">Médico</th>
            <th @click="sortTable('fecha')">Fecha</th>
            <th>Hora</th>
            <th @click="sortTable('estado')">Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cita in paginatedCitas" :key="cita.id_cita">
            <td>{{ cita.id_cita }}</td>
            <td>{{ cita.refcita }}</td>
            <td>{{ cita.paciente }}</td>
            <td>{{ cita.especialidad }}</td>
            <td>{{ cita.medico }}</td>
            <td>{{ formatFecha(cita.fecha) }}</td>
            <td>{{ cita.hora }}</td>
            <td>{{ cita.estado }}</td>
            <td>
              <button @click="editCita(cita)">Editar</button>
              <button @click="deleteCita(cita.id_cita)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Controles de paginación -->
    <div class="pagination">
      <button v-for="page in totalPages" :key="page" @click="changePage(page)"
        :class="{ active: currentPage === page }">
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script>


import axios from "axios";
import moment from 'moment';


export default {
  data() {
    return {
      citas: [],
      pacientes: [],
      medicos: [],
      currentPage: 1, // Página actual
      itemsPerPage: 10, // Registros por página
      isEditing: false,  // 🔔 Bandera para saber si estamos editando
      form: {
        id_cita: null,
        id_paciente: "",
        id_medico: "",
        especialidad: "",
        fecha: "",
        hora: "",
        refcita: "",
        estado: true,
      },
      sortKey: "",
      sortAsc: true,
      searchKey: "id_cita",
      searchValue: "",
    };
  },


  mounted() {
    this.fetchPacientes();
    this.fetchMedicos();
    this.fetchCitas();
  },


  watch: {
    // Detectar cambios en el valor de búsqueda
    searchValue() {
      this.currentPage = 1;  // Vuelve a la primera página al buscar
    },
    // Detectar cambios en el tipo de búsqueda
    searchKey() {
      this.currentPage = 1;  // Vuelve a la primera página al cambiar el filtro
    }
  },


  computed: {
    sortedCitas() {
      let filteredCitas = this.citas.map(cita => {
        return {
          id_cita: cita.id_cita,
          refcita: cita.refcita,
          paciente: `${cita.id_paciente.nombre} ${cita.id_paciente.apellido}`,
          medico: `${cita.id_medico.nombre}`,
          fecha: cita.fecha,
          hora: cita.hora,
          especialidad: cita.id_medico.especialidad,
          estado: cita.estado,
        };
      });

      if (this.searchValue.trim()) {
        filteredCitas = filteredCitas.filter(cita => {
          const value = cita[this.searchKey]?.toString().toLowerCase() || "";
          return value.includes(this.searchValue.toLowerCase());
        });
      }

      if (!this.sortKey) return filteredCitas;
      return filteredCitas.slice().sort((a, b) => {
        let result = 0;
        if (a[this.sortKey] < b[this.sortKey]) result = -1;
        if (a[this.sortKey] > b[this.sortKey]) result = 1;
        return this.sortAsc ? result : -result;
      });
    },

    // Calcular el total de páginas
    totalPages() {
      return Math.ceil(this.sortedCitas.length / this.itemsPerPage);
    },

    // Obtener los médicos de la página actual
    paginatedCitas() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedCitas.slice(start, end);
    },
  },


  methods: {

    changePage(page) {
      this.currentPage = page;
    },

    formatFecha(fecha) {
      if (!fecha) return 'Fecha inválida';
      return moment(fecha, ["YYYY-MM-DD", "DD-MM-YYYY"]).format("DD-MM-YYYY");
    },

    // ✅ Formatea la fecha a 'YYYY-MM-DD' antes de enviarla
    formatearFecha() {
      if (this.fecha) {
        const fechaSeleccionada = new Date(this.fecha);
        const año = fechaSeleccionada.getFullYear();
        const mes = String(fechaSeleccionada.getMonth() + 1).padStart(2, '0');
        const dia = String(fechaSeleccionada.getDate()).padStart(2, '0');

        this.cita.fecha = `${año}-${mes}-${dia}`;  // ✅ Formato YYYY-MM-DD
      }
    },


    actualizarFecha(event) {
      const fechaSeleccionada = event.target.value;  // Formato YYYY-MM-DD
      this.form.fecha = moment(fechaSeleccionada, "YYYY-MM-DD").format("DD-MM-YYYY");
    },


    searchCitas() {
      this.fetchCitas();
    },
    sortTable(key) {
      if (this.sortKey === key) {
        this.sortAsc = !this.sortAsc;
      } else {
        this.sortKey = key;
        this.sortAsc = true;
      }
    },


    getPacienteNombre(id_paciente) {
      if (!id_paciente) {
        alert("⚠️ ID del paciente no proporcionado.");
        return "Paciente no encontrado";
      }

      alert(`🔎 Buscando paciente con ID: ${id_paciente}`);

      const paciente = this.pacientes.find(p => p.id_paciente == id_paciente);

      if (!paciente) {
        alert(`❗ Paciente no encontrado. Lista de pacientes:\n${JSON.stringify(this.pacientes, null, 2)}`);
      }

      return paciente ? `${paciente.nombre} ${paciente.apellido}` : "Paciente no encontrado";
    },


    getMedicoEspecialidad(id_medico) {
      if (!id_medico) {
        alert("⚠️ ID del médico no proporcionado.");
        return "Especialidad no encontrada";
      }

      alert(`🔎 Buscando médico con ID: ${id_medico}`);

      const medico = this.medicos.find(m => m.id_medico == id_medico);

      if (!medico) {
        alert(`❗ Médico no encontrado. Lista de médicos:\n${JSON.stringify(this.medicos, null, 2)}`);
      }

      return medico ? medico.especialidad : "Especialidad no encontrada";
    },


    async fetchPacientes() {
      try {
        const response = await axios.get("/paciente/");
        this.pacientes = response.data;
      } catch (error) {
        console.error("Error al obtener pacientes:", error);
      }
    },

    async fetchMedicos() {
      try {
        const response = await axios.get("/medico/");
        this.medicos = response.data;
      } catch (error) {
        console.error("Error al obtener médicos:", error);
      }
    },

    async fetchCitas() {
      try {
        const response = await axios.get("/cita/");
        this.citas = response.data;
      } catch (error) {
        console.error("Error al obtener citas:", error);
      }
    },

    editCita(cita) {
      this.isEditing = true;  // Cambia a modo edición

      // Asignar valores con validación previa
      this.form = {
        id_cita: cita.id_cita,
        id_paciente: this.getPacienteNombre(cita.id_paciente),
        id_medico: this.getMedicoEspecialidad(cita.id_medico),
        fecha: cita.fecha,
        hora: cita.hora,
        estado: cita.estado === "confirmada",  // ✅ Convertir a booleano para el checkbox
        refcita: cita.refcita,
      };

      console.log("📝 Editando cita:", this.form);
    },

    getPacienteId(nombreCompleto) {
      const nombreFormateado = nombreCompleto.trim().toLowerCase();
      const paciente = this.pacientes.find(p =>
        `${p.nombre} ${p.apellido}`.trim().toLowerCase() === nombreFormateado
      );
      return paciente ? paciente.id_paciente : null;
    },


    async saveCita() {
      try {
        const payload = {
          id_cita: this.form.id_cita,
          id_paciente: this.getPacienteId(this.form.id_paciente),  // Recupera el ID
          id_medico: this.getMedicoId(this.form.id_medico),        // Recupera el ID del médico
          fecha: this.form.fecha,
          hora: this.form.hora,
          estado: this.form.estado ? "confirmada" : "pendiente",
          refcita: this.form.refcita,
        };

        await axios.put(`/cita/${payload.id_cita}`, payload);
        console.log("✅ Cita actualizada:", payload);
        this.isEditing = false;
        this.fetchCitas();  // Actualiza la lista de citas
      } catch (error) {
        console.error("❌ Error al guardar la cita:", error);
      }
    },


    editPaciente(cita) {
      this.form = { ...cita };
    },

    async handleSubmit() {
      try {
        // ✅ Validar datos antes de enviar
        if (!this.validateFormData()) return;

        // ✅ Generar refcita si no existe
        if (!this.form.refcita) {
          this.form.refcita = this.generateRefCita();
        }

        // ✅ Preparar los datos para enviar
        const formData = {
          id_cita: this.form.id_cita || null,
          id_paciente_id: parseInt(this.form.id_paciente),  // Asegurar que se envía el ID
          id_medico_id: parseInt(this.form.id_medico),      // Asegurar que se envía el ID
          especialidad: this.getEspecialidad(this.form.id_medico),
          fecha: this.form.fecha,
          hora: this.form.hora,
          estado: this.form.estado ? "confirmada" : "pendiente",
          //refcita: this.form.refcita,
        };

        // 📋 Mostrar los datos antes de enviar
        //🆔 Cita ID: ${formData.id_cita}
        //📑 Referencia Cita: ${formData.refcita}
        const datosParaEnviar = `
      📋 **Datos que se enviarán al backend:**
      🧑‍🦱 Paciente ID: ${formData.id_paciente_id}
      🩺 Médico ID: ${formData.id_medico_id}
      🏥 Especialidad: ${formData.especialidad}
      📅 Fecha: ${formData.fecha}
      ⏰ Hora: ${formData.hora}
      ✅ Cita confirmada: ${formData.estado}
    `;

        // Confirmar antes de enviar
        if (!confirm(datosParaEnviar)) {
          alert("🚫 Envío cancelado.");
          return;
        }

        // ✅ ÚNICO envío de datos al backend
        if (this.isEditing) {
          await axios.put(`/cita/${this.form.id_cita}/`, formData);
          alert("✅ Cita actualizada con éxito.");
        } else {
          await axios.post("/cita/", formData);
          alert("✅ Cita creada con éxito.");
        }

        // 🔄 Refrescar citas y limpiar formulario
        this.fetchCitas();
        this.resetForm();

      } catch (error) {
        // ❗ Manejar errores detalladamente
        if (error.response) {
          console.error("❌ Error de respuesta del servidor:", error.response.data);
          const mensajeError = Object.entries(error.response.data)
            .map(([campo, mensajes]) => `🔸 ${campo}: ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
            .join('\n');
          alert(`❌ Error al guardar la cita:\n${mensajeError}`);
        } else if (error.request) {
          console.error("❌ Error en la petición:", error.request);
          alert("❌ No se recibió respuesta del servidor.");
        } else {
          console.error("❌ Error inesperado:", error.message);
          alert(`❌ Error inesperado: ${error.message}`);
        }
      }
    },


    // 🔢 Generar referencia de cita automáticamente
    generateRefCita() {
      const fecha = moment().format("YYYYMMDDHHmm");
      return `${fecha}`;
    },

    validateFormData() {
      const errores = [];

      if (!this.form.id_paciente) errores.push("❗ El campo *Paciente* es obligatorio.");
      if (!this.form.id_medico) errores.push("❗ El campo *Especialidad/Médico* es obligatorio.");
      if (!this.form.fecha) errores.push("❗ El campo *Fecha* es obligatorio.");
      if (!this.form.hora) errores.push("❗ El campo *Hora* es obligatorio.");

      if (errores.length) {
        alert("⚠️ **Errores detectados:**\n" + errores.join('\n'));
        return false;
      }

      return true;
    },


    getEspecialidad(id_medico) {
      const medicoSeleccionado = this.medicos.find(medico => medico.id_medico === id_medico);
      return medicoSeleccionado ? medicoSeleccionado.especialidad : "";
    },


    async deleteCita(id_cita) {
      if (confirm("¿Estás seguro de eliminar esta cita?")) {
        try {
          await axios.delete(`/cita/${id_cita}/`);
          alert("Cita eliminada con éxito.");
          this.fetchCitas();
        } catch (error) {
          console.error("Error al eliminar la cita:", error.response?.data || error.message);
          alert("Hubo un error al eliminar la cita.");
        }
      }
    },
    resetForm() {
      this.isEditing = false;
      this.form = {
        id_cita: null,
        id_paciente: "",
        id_medico: "",
        fecha: "",
        hora: "",
        estado: "",
        refcita: "",
      };
    },
  },
};
</script>

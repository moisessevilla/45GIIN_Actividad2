<template>
  <div class="contenido">
    <h1>Gestión de Médicos</h1>

    <!-- Formulario para crear/editar médicos -->
    <form @submit.prevent="handleSubmit" class="formulario">
      <div class="form-group">
        <label for="ncolegiado">Nº Colegiado:*</label>
        <input id="ncolegiado" v-model="form.ncolegiado" type="text" minlength="6" maxlength="8"
          placeholder="Introduce número de colegiado" required />
      </div>
      <div class="form-group">
        <label for="nombre">Nombre:*</label>
        <input id="nombre" v-model="form.nombre" type="text" minlength="3" maxlength="100"
          placeholder="Introduce nombre del colegiado" required />
      </div>
      <div class="form-group">
        <label for="especialidad">Especialidad:*</label>
        <input id="especialidad" v-model="form.especialidad" type="text" minlength="3" maxlength="100"
          placeholder="Introduce la especialidad" required />
      </div>
      <div class="form-group">
        <label for="email">Email:*</label>
        <input id="email" v-model="form.email" type="email" @input="validateEmail" placeHolder="Ingrese un email válido"
          required />
      </div>
      <div class="info">
        <label for="info">* Campos requeridos.</label>
      </div>
      <div class="form-buttons">
        <button type="submit">{{ form.id_medico ? 'Actualizar' : 'Crear' }} Médico</button>
        <button type="button" v-if="form.id_medico" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <select v-model="searchKey" class="busqueda-select">
        <option value="id_medico">ID</option>
        <option value="ncolegiado">Nº Colegiado</option>
        <option value="nombre">Nombre</option>
        <option value="especialidad">Especialidad</option>
        <option value="email">Email</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>

    <!-- Tabla de médicos con scroll limitado a 5 registros y ordenación -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th @click="sortTable('id_medico')">ID</th>
            <th @click="sortTable('ncolegiado')">Nº Colegiado</th>
            <th @click="sortTable('nombre')">Nombre</th>
            <th @click="sortTable('especialidad')">Especialidad</th>
            <th @click="sortTable('email')">Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="medico in paginatedMedicos" :key="medico.id_medico">
            <td>{{ medico.id_medico }}</td>
            <td>{{ medico.ncolegiado }}</td>
            <td>{{ medico.nombre }}</td>
            <td>{{ medico.especialidad }}</td>
            <td>{{ medico.email }}</td>
            <td>
              <button @click="editMedico(medico)">Editar</button>
              <button @click="deleteMedico(medico.id_medico)">Eliminar</button>
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

export default {
  data() {
    return {
      medicos: [],
      currentPage: 1, // Página actual
      itemsPerPage: 10, // Registros por página
      form: {
        id_medico: null,
        ncolegiado: "",
        nombre: "",
        especialidad: "",
        email: "",
      },
      sortKey: '', // Clave por la que ordenar
      sortAsc: true, // Orden ascendente o descendente
      searchKey: 'nombre', // Clave para la búsqueda
      searchValue: '', // Valor para la búsqueda
    };
  },
  computed: {
    sortedMedicos() {
      let filteredMedicos = this.medicos;
      if (this.searchValue.trim()) {
        filteredMedicos = filteredMedicos.filter(medico => {
          const value = medico[this.searchKey]?.toString().toLowerCase() || '';
          return value.includes(this.searchValue.toLowerCase());
        });
      }
      if (!this.sortKey) return filteredMedicos;
      return filteredMedicos.slice().sort((a, b) => {
        let result = 0;
        if (a[this.sortKey] < b[this.sortKey]) result = -1;
        if (a[this.sortKey] > b[this.sortKey]) result = 1;
        return this.sortAsc ? result : -result;
      });
    },
    // Calcular el total de páginas
    totalPages() {
      return Math.ceil(this.sortedMedicos.length / this.itemsPerPage);
    },
    // Obtener los médicos de la página actual
    paginatedMedicos() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedMedicos.slice(start, end);
    },
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

  methods: {
    changePage(page) {
      this.currentPage = page;
    },
    // Validación de DNI (exactamente 8 dígitos seguidos de 1 letra)
    validateDNI(event) {
      const value = event.target.value.toUpperCase(); // Convierte a mayúsculas automáticamente

      // Permitir solo 8 dígitos numéricos seguidos de 1 letra (exactamente 9 caracteres)
      const dniRegex = /^\d{0,8}$/; // Solo dígitos hasta 8 caracteres
      const dniCompleteRegex = /^\d{8}[A-Z]$/; // Exactamente 8 dígitos seguidos de 1 letra

      // Validar los 8 primeros caracteres como dígitos numéricos
      if (value.length <= 8) {
        if (!dniRegex.test(value)) {
          this.form.dni = value.slice(0, -1); // Elimina el último carácter no válido
          this.dniError = "Solo se permiten números en los primeros 8 caracteres.";
          return;
        }
        this.dniError = "El DNI debe contener 8 dígitos seguidos de 1 letra.";
      }

      // Validar el noveno carácter como una letra
      if (value.length === 9) {
        const lastChar = value[8]; // Noveno carácter
        if (!/^[A-Z]$/.test(lastChar)) {
          this.form.dni = value.slice(0, 8); // Elimina el carácter si no es una letra
          this.dniError = "El último carácter debe ser una letra.";
          return;
        }
        this.dniError = dniCompleteRegex.test(value)
          ? ""
          : "El DNI debe contener 8 dígitos seguidos de 1 letra.";
      }

      // Limitar la longitud a 9 caracteres
      if (value.length > 9) {
        this.form.dni = value.slice(0, 9); // Recorta el valor a 9 caracteres
        return;
      }

      // Actualizar el valor del DNI si todo está correcto
      this.form.dni = value;

      // Si no está completo, mostrar error
      if (this.form.dni.length < 9) {
        event.target.setCustomValidity("El DNI debe contener exactamente 8 dígitos y 1 letra.");
      } else {
        event.target.setCustomValidity("");
      }
    },

    // Validación de Email (arroba y un punto)
    validateEmail(event) {
      const value = event.target.value;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Formato básico de email
      if (!emailRegex.test(value)) {
        event.target.setCustomValidity(
          "El email debe contener una '@' y un dominio con un punto (ejemplo: usuario@dominio.com)"
        );
      } else {
        event.target.setCustomValidity("");
      }
    },
    // Buscar médicos
    searchMedicos() {
      this.fetchMedicos(); // En caso de necesitar actualizar la lista completa
    },

    // Ordenar la tabla
    sortTable(key) {
      if (this.sortKey === key) {
        this.sortAsc = !this.sortAsc;
      } else {
        this.sortKey = key;
        this.sortAsc = true;
      }
    },

    // Obtener la lista de médicos
    async fetchMedicos() {
      try {
        const response = await axios.get("/medico/");
        this.medicos = response.data;
      } catch (error) {
        console.error("Error al obtener médicos:", error);
      }
    },

    // Crear o actualizar un médico
    async handleSubmit() {
      try {
        if (this.form.id_medico) {
          // Actualizar médico
          const updateData = {
            ncolegiado: this.form.ncolegiado,
            nombre: this.form.nombre,
            especialidad: this.form.especialidad,
            email: this.form.email,
          };

          await axios.put(`/medico/${this.form.id_medico}/`, updateData, {
            headers: { 'Content-Type': 'application/json' },
          });

          alert("Médico actualizado con éxito.");
        } else {
          // Crear médico
          await axios.post("/medico/", this.form, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
          alert("Médico creado con éxito.");
        }
        this.fetchMedicos();
        this.resetForm();
      } catch (error) {
        console.error("Error al guardar el especialista:", error.response?.data || error.message);

        // Validar si la respuesta es de tipo JSON
        if (error.response && error.response.headers['content-type'].includes('application/json')) {
          const errores = error.response.data;

          // Manejar múltiples errores
          const mensajeError = Object.entries(errores)
            .map(([campo, mensajes]) => `${campo}: ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
            .join('\n');

          alert(`Error al guardar el especialista:\n${mensajeError}`);

        } else if (typeof error.response?.data === 'string') {
          // Si la respuesta es texto o HTML
          alert(`Error inesperado:\n${error.response.data}`);

        } else {
          alert("Hubo un error al guardar el especialista.");
        }
      }
    },

    // Cargar datos del médico en el formulario para editar
    editMedico(medico) {
      this.form = { ...medico };
    },

    // Eliminar un médico
    async deleteMedico(id_medico) {
      if (confirm("¿Estás seguro de eliminar este médico?")) {
        try {
          await axios.delete(`/medico/${id_medico}/`, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
          alert("Médico eliminado con éxito.");
          this.fetchMedicos();
          //Módulo para refrescar páginas cuando se reducen de en una menos
          await this.fetchPacientes(); // Vuelve a cargar los pacientes después de eliminar

          // Si la página actual es mayor que el total de páginas, vuelve a la última página válida
          if (this.currentPage > this.totalPages) {
            this.currentPage = this.totalPages || 1; // Si no hay registros, vuelve a la página 1
          }
        } catch (error) {
          console.error("Error al eliminar el médico:", error.response ? error.response.data : error.message);
          alert("Hubo un error al eliminar el médico.");
        }
      }
    },

    // Reiniciar el formulario
    resetForm() {
      this.form = {
        id_medico: null,
        ncolegiado: "",
        nombre: "",
        especialidad: "",
        email: "",
      };
    },
  },
  mounted() {
    this.fetchMedicos();
  },
};
</script>

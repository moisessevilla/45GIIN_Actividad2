<template>
  <div class="contenido">
    <h1>Gestión de Pacientes</h1>

    <!-- Formulario para crear/editar pacientes -->
    <form @submit.prevent="handleSubmit" class="formulario">
      <div class="form-group">
        <label for="dni">DNI:*</label>
        <input id="dni" v-model="form.dni" type="text" maxlenght="9" @input="validateDNI"
          placeholder="Formato: 8 dígitos + 1 letra" required />
      </div>
      <div class="form-group">
        <label for="nombre">Nombre:*</label>
        <input id="nombre" v-model="form.nombre" minlength="3" maxlenght="100" type="text"
          placeholder="Mínimo 3 carácteres" required />
      </div>
      <div class="form-group">
        <label for="apellido">Apellido:*</label>
        <input id="apellido" v-model="form.apellido" minlength="3" maxlenght="100" type="text"
          placeholder="Mínimo 3 carácteres" required />
      </div>
      <div class="form-group">
        <label for="email">Email:*</label>
        <input id="email" v-model="form.email" type="email" @input="validateEmail" placeHolder="Ingrese un email válido"
          required />
      </div>
      <div class="form-group">
        <label for="telefono">Teléfono:*</label>
        <input id="telefono" v-model="form.telefono" type="text" maxlenght="9" @input="validateTelefono"
          placeholder="Ingrese un teléfono de 9 dígitos" required />
      </div>
      <div class="form-group">
        <label for="contrasena">Contraseña:*</label>
        <input id="contrasena" v-model="form.contrasena" minlength="6" maxlenght="100"
          placeholder="Ingrese un contraseña 6 cáracteres o más" :type="showPassword ? 'text' : 'password'"
          :required="!form.id_paciente" />
      </div>
      <!--
      <div class="checkbox-inline">
        <input type="checkbox" v-model="showPassword" />
        <label for="mostrar_contrasena"> Mostrar Contraseña</label>
      </div>
    -->
      <div class="info">
        <label for="info">* Campos requeridos.</label>
      </div>
      <div class="form-buttons">
        <button type="submit">{{ form.id_paciente ? 'Actualizar' : 'Crear' }} Paciente</button>
        <button type="button" v-if="form.id_paciente" @click="resetForm">Cancelar</button>
      </div>
    </form>

    <!-- Campo de búsqueda -->
    <div class="busqueda-container">
      <select v-model="searchKey" class="busqueda-select">
        <option value="id_paciente">ID</option>
        <option value="dni">DNI</option>
        <option value="nombre">Nombre</option>
        <option value="apellido">Apellido</option>
        <option value="email">Email</option>
        <option value="telefono">Teléfono</option>
      </select>
      <input type="text" v-model="searchValue" class="busqueda-input" placeholder="Ingrese criterio de búsqueda" />
    </div>

    <!-- Tabla de pacientes con scroll limitado a 7 registros y ordenación -->
    <div class="tabla-container">
      <table>
        <thead>
          <tr>
            <th @click="sortTable('id_paciente')">ID</th>
            <th @click="sortTable('dni')">DNI</th>
            <th @click="sortTable('nombre')">Nombre</th>
            <th @click="sortTable('apellido')">Apellido</th>
            <th @click="sortTable('email')">Email</th>
            <th @click="sortTable('telefono')">Teléfono</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="paciente in paginatedPacientes" :key="paciente.id_paciente">
            <td>{{ paciente.id_paciente }}</td>
            <td>{{ paciente.dni }}</td>
            <td>{{ paciente.nombre }}</td>
            <td>{{ paciente.apellido }}</td>
            <td>{{ paciente.email }}</td>
            <td>{{ paciente.telefono }}</td>
            <td class="acciones">
              <button @click="editPaciente(paciente)">Editar</button>
              <button @click="deletePaciente(paciente.id_paciente)">Eliminar</button>
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
      pacientes: [],
      currentPage: 1, // Página actual
      itemsPerPage: 10, // Registros por página
      form: {
        id_paciente: null,
        dni: "",
        nombre: "",
        apellido: "",
        email: "",
        telefono: "",
        contrasena: "",
      },
      showPassword: false, // Controla la visibilidad del campo contraseña
      sortKey: '', // Clave por la que ordenar
      sortAsc: true, // Orden ascendente o descendente
      searchKey: 'nombre', // Clave para la búsqueda
      searchValue: '', // Valor para la búsqueda
    };
  },
  computed: {
    sortedPacientes() {
      let filteredPacientes = this.pacientes;
      if (this.searchValue.trim()) {
        filteredPacientes = filteredPacientes.filter(paciente => {
          const value = paciente[this.searchKey]?.toString().toLowerCase() || '';
          return value.includes(this.searchValue.toLowerCase());
        });
      }
      if (!this.sortKey) return filteredPacientes;
      return filteredPacientes.slice().sort((a, b) => {
        let result = 0;
        if (a[this.sortKey] < b[this.sortKey]) result = -1;
        if (a[this.sortKey] > b[this.sortKey]) result = 1;
        return this.sortAsc ? result : -result;
      });
    },
    // Calcular el total de páginas
    totalPages() {
      return Math.ceil(this.sortedPacientes.length / this.itemsPerPage);
    },
    // Obtener los pacientes de la página actual
    paginatedPacientes() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedPacientes.slice(start, end);
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

    // Validación de Teléfono (exactamente 9 dígitos numéricos)
    validateTelefono(event) {
      const value = event.target.value.replace(/\D/g, ""); // Elimina caracteres no numéricos
      if (value.length > 9) {
        this.form.telefono = value.slice(0, 9); // Limita a 8 dígitos
      } else {
        this.form.telefono = value;
      }

      // Verifica si tiene menos de 9 dígitos
      if (this.form.telefono.length < 9) {
        event.target.setCustomValidity("El teléfono debe tener exactamente 9 dígitos.");
      } else {
        event.target.setCustomValidity("");
      }
    },


    // Buscar pacientes
    searchPacientes() {
      this.fetchPacientes(); // En caso de necesitar actualizar la lista completa
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

    // Obtener la lista de pacientes
    async fetchPacientes() {
      try {
        const response = await axios.get("/paciente/");
        this.pacientes = response.data;
      } catch (error) {
        console.error("Error al obtener pacientes:", error);
      }
    },

    // Crear o actualizar un paciente
    async handleSubmit() {
      try {
        if (this.form.id_paciente) {
          // Actualizar paciente
          const updateData = {
            dni: this.form.dni,
            nombre: this.form.nombre,
            apellido: this.form.apellido,
            email: this.form.email,
            telefono: this.form.telefono || null,
            contrasena: this.form.contrasena || undefined,
          };

          await axios.put(`/paciente/${this.form.id_paciente}/`, updateData);
          alert("Paciente actualizado con éxito.");
        } else {
          // Crear paciente
          const createData = {
            dni: this.form.dni,
            nombre: this.form.nombre,
            apellido: this.form.apellido,
            email: this.form.email,
            telefono: this.form.telefono || null,
            contrasena: this.form.contrasena,
          };

          const response = await axios.post("/paciente/", createData);
          alert(`Paciente creado con éxito. ID asignado: ${response.data.id_paciente}`);
        }
        this.fetchPacientes();
        this.resetForm();
      } catch (error) {
        console.error("Error al guardar el paciente:", error.response?.data || error.message);

        // Validar si la respuesta es de tipo JSON
        if (error.response && error.response.headers['content-type'].includes('application/json')) {
          const errores = error.response.data;

          // Manejar múltiples errores
          const mensajeError = Object.entries(errores)
            .map(([campo, mensajes]) => `${campo}: ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
            .join('\n');

          alert(`Error al guardar el paciente:\n${mensajeError}`);

        } else if (typeof error.response?.data === 'string') {
          // Si la respuesta es texto o HTML
          alert(`Error inesperado:\n${error.response.data}`);

        } else {
          alert("Hubo un error al guardar el paciente.");
        }
      }
    },

    // Cargar datos del paciente en el formulario para editar
    editPaciente(paciente) {
      this.form = { ...paciente };
    },

    // Eliminar un paciente
    async deletePaciente(id_paciente) {
      if (confirm("¿Estás seguro de eliminar este paciente?")) {
        try {
          await axios.delete(`/paciente/${id_paciente}/`, {
            headers: {
              'Content-Type': 'application/json',
            },
          });
          alert("Paciente eliminado con éxito.");
          this.fetchPacientes();

          //Módulo para refrescar páginas cuando se reducen de en una menos
          await this.fetchPacientes(); // Vuelve a cargar los pacientes después de eliminar

          // Si la página actual es mayor que el total de páginas, vuelve a la última página válida
          if (this.currentPage > this.totalPages) {
            this.currentPage = this.totalPages || 1; // Si no hay registros, vuelve a la página 1
          }

        } catch (error) {
          console.error("Error al guardar el paciente:", error.response?.data || error.message);

          if (error.response?.data) {
            const errores = error.response.data;

            // Manejar múltiples errores y mostrarlos claramente
            const mensajeError = Object.entries(errores)
              .map(([campo, mensajes]) => `${campo}: ${Array.isArray(mensajes) ? mensajes.join(', ') : mensajes}`)
              .join('\n');

            alert(`Error al guardar el paciente:\n${mensajeError}`);
          } else {
            alert("Hubo un error al guardar el paciente.");
          }
        }

      }
    },

    // Reiniciar el formulario
    resetForm() {
      this.form = {
        id_paciente: null,
        dni: "",
        nombre: "",
        apellido: "",
        email: "",
        telefono: "",
        contrasena: "",
      };
    },
  },
  mounted() {
    this.fetchPacientes();
  },
};
</script>
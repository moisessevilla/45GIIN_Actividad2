<template>
  <div class="welcome-header">
    <h1>Bienvenido a la Clínica Rehabilita tu alma</h1>
  </div>
  <div class="login-container">
    <div class="login-card">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" placeholder="Ingresa tu email" required />
        </div>
        <div class="input-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" placeholder="Ingresa tu contraseña" required />
        </div>
        <div class="button-container">
          <button type="submit" class="btn-submit">Entrar</button>
        </div>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post("http://localhost:8000/api/login/", {
          email: this.email,
          password: this.password,
        });
        this.$cookies.set("auth_token", response.data.token, "1d");
        this.$router.push("/dashboard");
      } catch (error) {
        this.errorMessage = "Correo o contraseña incorrectos. Intenta nuevamente.";
      }
    },
  },
};
</script>

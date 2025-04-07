<template>
  <div class="container">
    <h1 class="title">AUTHENTICATION</h1>
    <div class="form-container">
      <div class="form-box" v-if="showLogin">
        <h2>Login</h2>
        <button @click="navigateBack">Back</button>
        <input type="text" placeholder="Username" v-model="loginUsername" />
        <input type="password" placeholder="Password" v-model="loginPassword" />
        <button class="btn login" @click="check_login">Login</button>
        <p>Don't have an account? <span @click="toggleForm">Register here</span></p>
      </div>

      <div class="form-box" v-else>
        <h2>Register</h2>
        <button @click="navigateBack">Back</button>
        <input type="text" placeholder="Username" v-model="registerUsername" />
        <input type="password" placeholder="Password" v-model="registerPassword" />
        <button class="btn register" @click="register">Register</button>
        <p>Already have an account? <span @click="toggleForm">Login here</span></p>
      </div>
    </div>

    <p v-if="message.error" class="error-message">{{ message.error }}</p>
    <p v-if="message.success" class="success-message">{{ message.success }}</p>
  </div>
</template>

<script>
import toastr from 'toastr';
import 'toastr/build/toastr.min.css';

export default {
  name: "authentication",

  data() {
    return {
      showLogin: true,
      loginUsername: '',
      loginPassword: '',
      registerUsername: '',
      registerPassword: '',
      client_socket: this.$store.state.currentClientSocket,
      message: { error: "", success: "" },
    };
  },

  mounted() {
    this.setupSocketListeners();
  },

  unmounted() {
    this.removeSocketListeners();
  },

  methods: {
    toggleForm() {
      this.clearMessages();
      this.resetInputs();
      this.showLogin = !this.showLogin;
    },

    clearMessages() {
      this.message.error = "";
      this.message.success = "";
    },

    resetInputs() {
      this.loginUsername = '';
      this.loginPassword = '';
      this.registerUsername = '';
      this.registerPassword = '';
    },

    navigateBack() {
      this.next_page('main');
    },

    check_login() {
      this.client_socket.emit('check-login', this.loginUsername);
    },

    async login() {
      this.clearMessages();

      if (!this.validateLoginInputs()) return;

      this.message.success = "Logging in ...";

      const response = await this.azure_function('POST', '/user/login', {
        username: this.loginUsername,
        password: this.loginPassword,
      });

      if (response.msg === "OK" && response.result) {
        this.message.success = "Successfully logged in! Loading Account Stats ...";
        this.$store.commit("setCurrentUser", this.loginUsername);
        this.$store.commit("setCurrentPassword", this.loginPassword);

        await this.retrieve_user_info(this.loginUsername);

        this.client_socket.emit('login', this.loginUsername);
        this.next_page('dashboard');
      } else {
        this.message.error = response.msg || "Login failed.";
      }

      this.resetInputs();
    },

    async register() {
      this.clearMessages();

      if (!this.validateRegisterInputs()) return;

      this.message.success = "Registering user ...";

      const response = await this.azure_function('POST', '/user/register', {
        username: this.registerUsername,
        password: this.registerPassword,
      });

      if (response.msg === "OK" && response.result) {
        this.message.success = "Successfully registered! You may now login.";
      } else {
        this.message.error = response.msg || "Registration failed.";
      }

      this.resetInputs();
    },

    validateLoginInputs() {
      if (this.loginUsername.length < 5 || this.loginUsername.length > 15) {
        this.message.error = "Username must be between 5 and 15 characters.";
        return false;
      }
      if (this.loginPassword.length < 8 || this.loginPassword.length > 15) {
        this.message.error = "Password must be between 8 and 15 characters.";
        return false;
      }
      return true;
    },

    validateRegisterInputs() {
      if (this.registerUsername.length < 5 || this.registerUsername.length > 15) {
        this.message.error = "Username must be between 5 and 15 characters.";
        return false;
      }
      if (this.registerPassword.length < 8 || this.registerPassword.length > 15) {
        this.message.error = "Password must be between 8 and 15 characters.";
        return false;
      }
      return true;
    },

    async retrieve_user_info(username) {
      const response = await this.azure_function('POST', '/user/get/info', { username });
      if (response.result) {
        const info = response.msg;
        this.$store.commit("setCurrentRank", info.rank);
        this.$store.commit("setCurrentStats", {
          id: info.id,
          streak: info.streak,
          daily_training_score: info.daily_training_score,
          training_completion_date: info.training_completion_date,
        });
        this.$store.commit("setCurrentAchievements", info.achievements);

        if (info.achievements.length === 0) {
          this.add_achievement('Hello World!');
        }
      } else {
        this.message.error = response.msg || "Loading failed.";
      }
    },

    async add_achievement(name) {
      const user_stats = this.$store.state.currentStats;
      const achievements = [...this.$store.state.currentAchievements, name];
      const input = { id: user_stats.id, updates: { achievements } };

      const update = await this.azure_function("PUT", "/user/update/info", input);
      if (update) {
        this.$store.commit("setCurrentAchievements", achievements);
        this.message.success = 'Achievements update Successful!';

        toastr.success(`"${name}"`, "Achievement Unlocked:", {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-top-right",
          timeOut: 5000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut"
        });
      }
    },

    async azure_function(method, route, data) {
      try {
        console.log(route);
        const url = `${process.env.VUE_APP_BACKEND_URL}${route}?code=${process.env.VUE_APP_MASTER_KEY}`;
        const response = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        return await response.json();
      } catch (error) {
        console.error("API Error:", error);
        this.message.error = "An API error occurred. Please try again later.";
      }
    },

    next_page(page) {
      this.$router.push(`/${page}`);
    },

    setupSocketListeners() {
      if (!this.client_socket) return;

      this.client_socket.on('check-login-successful', this.login);
      this.client_socket.on('check-login-fail', () => {
        this.message.error = "User is already logged in";
      });
    },

    removeSocketListeners() {
      if (!this.client_socket) return;

      this.client_socket.off('check-login-successful');
      this.client_socket.off('check-login-fail');
    },
  },
};
</script>

<style lang="scss" scoped>
/* Add your scoped styles here */
</style>
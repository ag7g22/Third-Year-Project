<template>
  <div class="auth-container">
    <!-- Left side: Empty or can contain an image -->
    <div class="left-side">
      <div class="form-container">
        <h3>Welcome to GearUp!</h3>
        <p>The ultimate way to make driving theory prep actually enjoyable.
          Whether you're just starting out or brushing up before the big test, GearUp! transforms dry material into a fun, interactive learning experience. 
          No more boring textbooks or endless note-taking — just engaging quizzes, bite-sized challenges, and real-time progress tracking that keeps you motivated.</p>
          <div class="feature-list">
            <p>✅ Daily quizzes to keep your brain sharp</p>
            <p>✅ Category-specific practice</p>
            <p>✅ Mock exams that feel just like the real thing</p>
            <p>✅ Compete with friends on leaderboards</p>
            <p>✅ Earn achievements as you hit milestones</p>
            <p>✅ Track your stats and improve over time</p>
          </div>
          <p>Whether you're studying solo or racing your friends to the finish line, you'll be ready to SMASH the theory test!</p>
        <button @click="navigateBack" class="left-button">Back</button>
      </div>
    </div>
    
    <!-- Right side: Contains the form -->
    <div class="right-side">
      <div class="form-container">
        <div class="form-box" v-if="showLogin">
          <h2>Login to your account</h2>
          <p><span>username</span></p>
          <input type="text" placeholder="Username" v-model="loginUsername" />
          <div v-if="showPassword">
            <p><span @click="toggle_password">hide password</span></p>
            <input type="text" placeholder="Password" v-model="loginPassword" />
          </div>
          <div v-else>
            <p><span @click="toggle_password">show password</span></p>
            <input type="password" placeholder="Password" v-model="loginPassword" />
          </div>
          <div>
            <div v-if="sentRequest">
              <button class="right-button" disabled>Loading ...</button>
            </div>
            <div v-else>
              <button class="right-button" @click="check_login">Login</button>
            </div>
            <p>Don't have an account? <span @click="toggle_form">Register here</span></p>
          </div>
        </div>

        <div class="form-box" v-else>
          <h2>Register a NEW account</h2>
          <p><span>username</span></p>
          <input type="text" placeholder="Username" v-model="registerUsername" />
          <div v-if="showPassword">
            <p><span @click="toggle_password">hide password</span></p>
            <input type="text" placeholder="Password" v-model="registerPassword" />
          </div>
          <div v-else>
            <p><span @click="toggle_password">show password</span></p>
            <input type="password" placeholder="Password" v-model="registerPassword" />
          </div>
          <div>
          <div v-if="sentRequest">
            <button class="right-button" disabled>Loading ...</button>
          </div>
          <div v-else>
            <button class="right-button" @click="register">Register</button>
          </div>
            <p>Already have an account? <span @click="toggle_form">Login here</span></p>
          </div>
        </div>
      </div>
    </div>
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
      showPassword: false,
      sentRequest: false,
      loginUsername: '',
      loginPassword: '',
      registerUsername: '',
      registerPassword: '',
      client_socket: this.$store.state.currentClientSocket,
    };
  },
  mounted() {
    this.setup_socket_listeners();
  },
  unmounted() {
    this.remove_socket_listeners();
  },
  methods: {
    toggle_form() {
      this.reset_inputs();
      this.showLogin = !this.showLogin;
    },
    toggle_password() {
      this.showPassword = !this.showPassword;
    },
    reset_inputs() {
      this.sentRequest = false;
      this.loginUsername = '';
      this.loginPassword = '';
      this.registerUsername = '';
      this.registerPassword = '';
    },
    navigateBack() {
      this.next_page('');
    },
    check_login() {
      this.sentRequest = true;
      console.log('Notifying server ...');
      this.client_socket.emit('check-login', this.loginUsername);
    },
    successful_message(title, msg) {
        toastr.success(msg, title, {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-bottom-full-width",
          timeOut: 5000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut",
          preventDuplicates: true
        });
    },
    error_message(title, msg) {
      toastr.error(msg, title, {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-bottom-full-width",
          timeOut: 5000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut",
          preventDuplicates: true
        });
    },
    async login() {
      if (!this.validateLoginInputs()) return;

      const response = await this.azure_function('POST', '/user/login', {
        username: this.loginUsername,
        password: this.loginPassword,
      });

      if (response.msg === "OK" && response.result) {
        this.$store.commit("setCurrentUser", this.loginUsername);
        this.$store.commit("setCurrentPassword", this.loginPassword);

        await this.retrieve_user_info(this.loginUsername);

        this.client_socket.emit('login', this.loginUsername);
        this.next_page('dashboard');
      } else {
        const message = response.msg || "API error.";
        this.error_message("Login failed!", message);
      }
      this.reset_inputs();
    },
    async register() {
      this.sentRequest = true;

      if (!this.validateRegisterInputs()) return;

      const response = await this.azure_function('POST', '/user/register', {
        username: this.registerUsername,
        password: this.registerPassword,
      });

      if (response.msg === "OK" && response.result) {
        this.successful_message('Register success!', 'You may now login.');
      } else {
        const message = response.msg || "API error.";
        this.error_message("Register failed!", message);
      }
      this.reset_inputs();
    },
    validateLoginInputs() {
      if (this.loginUsername.length < 5 || this.loginUsername.length > 15) {
        this.error_message("Login failed!", "Username must be between 5 and 15 characters.");
        this.reset_inputs();
        return false;
      }
      if (this.loginPassword.length < 8 || this.loginPassword.length > 15) {
        this.error_message("Login failed!", "Password must be between 8 and 15 characters.");
        this.reset_inputs();
        return false;
      }
      return true;
    },
    validateRegisterInputs() {
      if (this.registerUsername.length < 5 || this.registerUsername.length > 15) {
        this.error_message("Register failed!", "Username must be between 5 and 15 characters.");
        this.reset_inputs();
        return false;
      }
      if (this.registerPassword.length < 8 || this.registerPassword.length > 15) {
        this.error_message("Register failed!", "Password must be between 8 and 15 characters.");
        this.reset_inputs();
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
        const message = response.msg || "Failed to load account stats.";
        this.error_message("Account error", message)
      }
    },
    async add_achievement(name) {
      const user_stats = this.$store.state.currentStats;
      const achievements = [...this.$store.state.currentAchievements, name];
      const input = { id: user_stats.id, updates: { achievements } };

      const update = await this.azure_function("PUT", "/user/update/info", input);
      if (update) {
        this.$store.commit("setCurrentAchievements", achievements);
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
      }
    },
    next_page(page) {
      this.$router.push(`/${page}`);
    },
    setup_socket_listeners() {
      if (!this.client_socket) return;

      this.remove_socket_listeners(); // Clean slate

      this.client_socket.on('check-login-successful', this.login);
      this.client_socket.on('check-login-fail', () => {
        this.error_message('Login failed!', 'Username or password incorrect');
      });
    },
    remove_socket_listeners() {
      if (!this.client_socket) return;

      this.client_socket.off('check-login-successful');
      this.client_socket.off('check-login-fail');
    },
  },
};
</script>

<style lang="scss" scoped>
.auth-container {
  display: flex;
  height: calc(100vh - 80px); /* 100% of the screen height minus the header's height */
  background-color: rgb(21, 0, 56); /* Dark background */
}

.left-side {
  flex: 1; /* Takes up the left side space */
  background-color: #000000; /* Optional: Black background */
  flex-direction: column;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 24px;
}

.feature-list {
  text-align: left;
  max-width: 600px;
  margin: 0 auto; /* Center the block itself while keeping text left-aligned */
  font-size: 16px;
  line-height: 1.6;
}

.right-side {
  flex: 1; /* Takes up the right side space */
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Ensures the form takes up the full height */
  align-items: center;
  background-color: rgb(21, 0, 56); /* Dark background */
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
}

.form-container {
  width: 100%;
  max-width: 500px; /* Limit the form width */
  border-radius: 10px;
  padding: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centers form content vertically */
  height: 100%; /* Ensure form takes up all vertical space in the right side */
  min-height: 300px; /* Minimum height for the form */
  background-color: transparent; /* Make the background transparent */
}

.form-container > * {
  visibility: visible; /* Ensure contents are visible */
}

h2 {
  text-align: center;
  color: #f3af59;
  font-size: 24px;
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #f3af59;
  border-radius: 5px;
  background-color: rgb(0, 0, 0);
  color: white;
  font-size: 16px;
}

input:focus {
  outline: none;
  border-color: #f3af59;
}

.left-button {
  color: #f3af59; /* Set the text color to the original color */
  font-size: 25px; /* Increase the font size */
  border: none; /* Remove the border */
  background: none; /* Remove the background */
  margin-top: 30px;
  cursor: pointer;
}

.left-button:hover {
  color: #fff; /* Change text color to white on hover */
  font-size: 26px; /* Increase the font size */
}

.right-button {
  width: 100%;
  padding: 12px;
  background-color: #f3af59;
  border: none;
  border-radius: 5px;
  color: white;
  font-size: 18px;
  cursor: pointer;
  margin-bottom: 20px;
}

.right-button:hover {
  background-color: #e09548; /* Hover effect for the button */
}

.right-button:disabled {
  background-color: #5c5c5c;
}

p {
  font-size: 14px;
  text-align: center;
  color: white;
}

span {
  color: #f3af59;
  cursor: pointer;
  text-decoration: underline;
}

.error-message {
  color: red;
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
}

.success-message {
  color: green;
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
}

form-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 30px;  /* Adds spacing between the items in the form container */
}

</style>
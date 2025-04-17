<template>
  <div class="split-container">
    <!-- INTRO Information about the app here -->
    <div class="left-side">
      <div class="instructions-container">
        <h3>Welcome to GearUp!</h3>
          <div class="feature-list">
            <p>The ultimate way to make driving theory prep actually enjoyable.
                Whether you're just starting out or brushing up before the big test, GearUp! transforms dry material into a fun, interactive learning experience. 
                No more boring textbooks or endless note-taking — just engaging quizzes, bite-sized challenges, and real-time progress tracking that keeps you motivated.</p>
          </div>
          <div class="feature-list">
            <p>✅ Daily quizzes to keep your brain sharp</p>
            <p>✅ Category-specific practice</p>
            <p>✅ Mock exams that feel just like the real thing</p>
            <p>✅ Compete with friends on leaderboards</p>
            <p>✅ Earn achievements as you hit milestones</p>
            <p>✅ Track your stats and improve over time</p>
          </div>
          <p>Whether you're studying solo or racing your friends to the finish line, you'll be ready to SMASH the theory test!</p>
      </div>
      <button @click="next_page('')" class="game-button">Back</button>
    </div>

    <div class="right-side">
      <div class="form-container">
        <!-- LOGIN FORM -->
        <div class="form-box" v-if="show_login">
          <h2>Login to your account</h2>
          <p><span>username</span></p>
          <input type="text" placeholder="Username" v-model="login_username"/>
          <div v-if="show_password">
            <p><span @click="toggle_password">hide password</span></p>
            <input type="text" placeholder="Password" v-model="login_password"/>
          </div>
          <div v-else>
            <p><span @click="toggle_password">show password</span></p>
            <input type="password" placeholder="Password" v-model="login_password"/>
          </div>
          <div>
            <div v-if="sent_request">
              <button class="request-button" disabled>Loading ...</button>
            </div>
            <div v-else>
              <button class="request-button" @click="check_login">Login</button>
            </div>
            <p>Don't have an account? <span @click="toggle_form">Register here</span></p>
          </div>
        </div>
        <!-- REGISTER FORM -->
        <div class="form-box" v-else>
          <h2>Register a NEW account</h2>
          <p><span>username</span></p>
          <input type="text" placeholder="Username" v-model="register_username" />
          <div v-if="show_password">
            <p><span @click="toggle_password">hide password</span></p>
            <input type="text" placeholder="Password" v-model="register_password" />
          </div>
          <div v-else>
            <p><span @click="toggle_password">show password</span></p>
            <input type="password" placeholder="Password" v-model="register_password" />
          </div>
          <div>
          <div v-if="sent_request">
            <button class="request-button" disabled>Loading ...</button>
          </div>
          <div v-else>
            <button class="request-button" @click="register">Register</button>
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
export default {
  name: "authentication",
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      show_login: true,
      show_password: false,
      sent_request: false,
      login_username: '',
      login_password: '',
      register_username: '',
      register_password: '',
    };
  },
  mounted() {
    this.setup_socket_listeners();
  },
  unmounted() {
    this.remove_socket_listeners();
  },
  methods: {
    // Check if the user hasn't done the daily quiz yet.
    daily_quiz_reminder() {
      const today = new Date();
        today.setHours(0, 0, 0, 0);
        const date = new Date(this.$store.state.currentStats.training_completion_date);
        if ((date.getFullYear() !== today.getFullYear() || date.getMonth() !== today.getMonth() || date.getDate() !== today.getDate()) ||
            (this.$store.state.currentStats.training_completion_date === 'n/a')) {
          toastr.error("Don't lose your streak >:(", `DO YOUR DAILY QUIZ!`, {
            closeButton: true,
            progressBar: true,
            positionClass: "toast-top-right",
            timeOut: 6000,
            showMethod: "fadeIn",
            hideMethod: "fadeOut",
            preventDuplicates: true
          });
        }
    },
    // Notfication message for a successful action.
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
    // Notification message for an error.
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
    // Toggles between register and login forms
    toggle_form() {
      this.reset_inputs();
      this.show_login = !this.show_login;
    },
    // Toggle flag whether to show password or not.
    toggle_password() {
      this.show_password = !this.show_password;
    },
    // Remove the inputs in the username and password forms.
    reset_inputs() {
      this.sent_request = false;
      this.login_username = '';
      this.login_password = '';
      this.register_username = '';
      this.register_password = '';
    },
    // Check with server if the user has logged in already or not.
    check_login() {
      this.sent_request = true;
      this.client_socket.emit('check-login', this.login_username);
    },
    // Check login details with the cosmos 'users' database and LOGIN
    async login() {
      if (!this.validate_login_inputs()) return;

      const response = await this.azure_function('POST', '/user/login', {
        username: this.login_username,
        password: this.login_password,
      });

      if (response.msg === "OK" && response.result) {
        this.$store.commit("setCurrentUser", this.login_username);
        this.$store.commit("setCurrentPassword", this.login_password);

        await this.retrieve_user_info(this.login_username);

        this.client_socket.emit('login', this.login_username);
        this.next_page('dashboard');
      } else {
        this.error_message("Register failed!", response.msg);
      }
      this.reset_inputs();
    },
    // Check register details with the cosmos database and add it.
    async register() {
      this.sent_request = true;

      if (!this.validate_register_inputs()) return;

      const response = await this.azure_function('POST', '/user/register', {
        username: this.register_username,
        password: this.register_password,
      });

      if (response.msg === "OK" && response.result) {
        this.successful_message('Register success!', 'You may now login.');
      } else {
        this.error_message("Register failed!", response.msg);
      }
      this.reset_inputs();
    },
    validate_login_inputs() {
      if (this.login_username.length < 5 || this.login_username.length > 15) {
        this.error_message("Login failed!", "Username must be between 5 and 15 characters.");
        this.reset_inputs();
        return false;
      }
      if (this.login_password.length < 8 || this.login_password.length > 15) {
        this.error_message("Login failed!", "Password must be between 8 and 15 characters.");
        this.reset_inputs();
        return false;
      }
      return true;
    },
    validate_register_inputs() {
      if (this.register_username.length < 5 || this.register_username.length > 15) {
        this.error_message("Register failed!", "Username must be between 5 and 15 characters.");
        this.reset_inputs();
        return false;
      }
      if (this.register_password.length < 8 || this.register_password.length > 15) {
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
        this.$store.commit("setCurrentRecentCatScores", info.recent_category_scores);

        if (info.achievements.length === 0) {
          this.add_achievement('Start of a Journey', '🔑');
        }
        
        this.daily_quiz_reminder();
      }
    },
    async add_achievement(name, emoji) {
      // Add an achievement in the user's data!
      if (this.$store.state.currentAchievements.includes(name)) {
        console.log(name + " achievement already unlocked.");
        return;
      }
      const user_stats = this.$store.state.currentStats;
      const achievements = [...this.$store.state.currentAchievements, name];
      const input = { id: user_stats.id, updates: { achievements } };
      const update = await this.azure_function("PUT", "/user/update/info", input);
      if (update) {
        this.$store.commit("setCurrentAchievements", achievements);
        toastr.success(`${name} ${emoji}`, "Achievement Unlocked:", {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-top-right",
          timeOut: 10000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut"
        });
      }
    },
    async azure_function(method, route, body) {
      // Send a request to the function app.
      console.log(route);
      const url = `${process.env.VUE_APP_BACKEND_URL}${route}?code=${process.env.VUE_APP_MASTER_KEY}`;
      try {
        const options = {
          method,
          headers: { "Content-Type": "application/json" },
        };
        if (method !== "GET") options.body = JSON.stringify(body);
        const response = await fetch(url, options);
        const result = await response.json();
        console.log("Result:", JSON.stringify(result.result));
        return result;
      } catch (error) {
        console.error("Error:", error);
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
        this.reset_inputs();
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
.form-container {
  width: 100%;
  max-width: 500px; /* Limit the form width */
  border-radius: 10px;
  padding: 40px;
  background-color: none;
  display: flex;
  flex-direction: column;
  justify-content: center; /* Centers form content vertically */
  height: 100%; /* Ensure form takes up all vertical space in the right side */
  min-height: 300px; /* Minimum height for the form */
}

h2 {
  text-align: center;
  color: #f3af59;
  font-size: 24px;
  margin-bottom: 20px;
}

.request-button {
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

.request-button:hover {
  background-color: #e09548; /* Hover effect for the button */
}

.request-button:disabled {
  background-color: #5c5c5c;
}

span {
  color: #f3af59;
  cursor: pointer;
  text-decoration: underline;
}

form-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 30px;  /* Adds spacing between the items in the form container */
}

</style>
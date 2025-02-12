<template>
  <div class="container">
    <h1 class="title">AUTHENTICATION</h1>
    <div class="form-container">
      <div class="form-box" v-if="showLogin">
        <h2>Login</h2>
        <button @click="next_page('main')">Back</button>
        <input type="text" placeholder="Username" v-model="loginUsername" />
        <input type="text" placeholder="Password" v-model="loginPassword" />
        <button class="btn login" @click="login">Login</button>
        <p>Don't have an account? <span @click="toggleForm">Register here</span></p>
      </div>
      <div class="form-box" v-else>
        <h2>Register</h2>
        <button @click="next_page('main')">Back</button>
        <input type="text" placeholder="Username" v-model="registerUsername" />
        <input type="text" placeholder="Password" v-model="registerPassword" />
        <button class="btn register" @click="register">Register</button>
        <p>Already have an account? <span @click="toggleForm">Login here</span></p>
      </div>
    </div>
    <p v-if="message.error" class="error-message">{{ message.error }}</p>
    <p v-if="message.success" class="success-message">{{ message.success }}</p>
  </div>
</template>

<script>
export default {
  name: "authentication",
  data() {
    return {
      showLogin: true,
      loginUsername: '',
      loginPassword: '',
      registerUsername: '',
      registerPassword: '',
      message: { error: "", success: "" }
    };
  },
  methods: {
    toggleForm() {
      // Reset messages
      this.message.error = "";
      this.message.success = "";

      // Reset Inputs
      this.loginUsername = "";
      this.loginPassword = "";
      this.registerUsername = "";
      this.registerPassword = "";

      this.showLogin = !this.showLogin;
    },
    async login() {
      // Reset messages
      this.message.error = "";
      this.message.success = "";

      // Validate form inputs
      if (this.loginUsername.length < 5 || this.loginUsername.length > 15) {
        this.message.error = "Username must be between 5 and 15 characters.";
        return;
      }

      if (this.loginPassword.length < 8 || this.loginPassword.length > 15) {
        this.message.error = "Password must be between 8 and 15 characters.";
        return;
      }
      
      const response = await this.POST_azure_function('/user/login', {"username": this.loginUsername , "password" : this.loginPassword})

      if (response.msg == "OK" && response.result) {
          this.message.success = "Successfully logged in! Loading Account Stats ...";
          this.$store.commit("setCurrentUser", this.loginUsername);
          this.$store.commit("setCurrentPassword", this.loginPassword);

          // GET USER STATS:
          this.retrieve_stats(this.$store.state.currentUser);

          console.log("Logged in as Current User and Password:", this.$store.state.currentUser, this.$store.state.currentPassword);

          this.next_page('dashboard');
      } else {
        this.message.error = response.msg || "Login failed.";
      }

      // Reset Inputs
      this.loginUsername = "";
      this.loginPassword = "";

    },
    async register() {
      // Reset messages
      this.message.error = "";
      this.message.success = "";

      // Validate form inputs
      if (this.registerUsername.length < 5 || this.registerUsername.length > 15) {
        this.message.error = "Username must be between 5 and 15 characters.";
        return;
      }

      if (this.registerPassword.length < 8 || this.registerPassword.length > 15) {
        this.message.error = "Password must be between 8 and 15 characters.";
        return;
      }

      const response = await this.POST_azure_function('/user/register', {"username": this.registerUsername , "password" : this.registerPassword});

      if (response.msg == "OK" && response.result) {
          this.message.success = "Successfully registered! You may now login.";
      } else {
        this.message.error = response.msg || "Registration failed.";
      }

      // Reset Inputs
      this.registerUsername = "";
      this.registerPassword = "";

    },
    async retrieve_stats(username) {
      // This retrieves the current stats of the logged in user:
      const user_stats = this.$store.state.currentStats;

      if (JSON.stringify(user_stats) === JSON.stringify({ id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a' })) {
        const response = await this.POST_azure_function('/user/get/info', {"username": username});
        if (response.result) { 
          const info = response.msg;
          const stats = { id: info.id, streak: info.streak, daily_training_score: info.daily_training_score, training_completion_date: info.training_completion_date}

          this.$store.commit("setCurrentStats", stats);
        } else {
          this.message.error = response.msg || "Loading failed.";
        }
      }
    },
    async POST_azure_function(function_route, json_doc) {
      console.log("Calling API request: " + function_route + ", params: " + JSON.stringify(json_doc));
      // Call Azure function with POST request
      try {
        const url = process.env.VUE_APP_BACKEND_URL + function_route + '?code=' + process.env.VUE_APP_MASTER_KEY
        const response = await fetch( url, { method: "POST", headers: { "Content-Type": "application/json"},body: JSON.stringify(json_doc)});
        const API_reply = await response.json();
        console.log("API Response: " + JSON.stringify(API_reply));
        return API_reply
      } catch (error) {
        console.error("API error:", error);
        this.message.error = "An API error occurred. Please try again later.";
      }
    },
    next_page(page) {
      console.log("Moving on to the " + page + " page!");
      this.$router.push(`/${page}`);
    }
  }
};
</script>

  <style lang="scss" scoped>
</style>
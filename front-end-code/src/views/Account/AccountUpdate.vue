<template>
    <div class="container">
      <h1 class="title">UPDATE DETAILS</h1>
  
      <div class="form-box">
        <h2>{{ showChangeUsername ? 'Change Username' : 'Change Password' }}</h2>
        <button @click="next_page('main')">Back</button>
  
        <template v-if="showChangeUsername">
          <input type="text" placeholder="New Username" v-model="form.new_username" />
          <input type="text" placeholder="Confirm Username" v-model="form.new_confirm_username" />
        </template>
  
        <template v-else>
          <input type="text" placeholder="New Password" v-model="form.new_password" />
          <input type="text" placeholder="Confirm Password" v-model="form.new_confirm_password" />
        </template>
  
        <button @click="toggleForm">
          {{ showChangeUsername ? 'Change Password' : 'Change Username' }}
        </button>
        <button @click="showChangeUsername ? confirmUsername() : confirmPassword()">Confirm</button>
      </div>
  
      <div class="buttons">
        <button @click="next_page('account')">Back</button>
      </div>
  
      <p v-if="message.error" class="error-message">{{ message.error }}</p>
      <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "update",
    data() {
      return {
        showChangeUsername: true,
        form: {
          new_username: "",
          new_password: "",
          new_confirm_username: "",
          new_confirm_password: ""
        },
        message: {
          error: "",
          success: ""
        }
      };
    },
    methods: {
      toggleForm() {
        this.message = { error: "", success: "" };
        this.form = {
          new_username: "",
          new_password: "",
          new_confirm_username: "",
          new_confirm_password: ""
        };
        this.showChangeUsername = !this.showChangeUsername;
      },
      async confirmUsername() {
        this.message = { error: "", success: "" };
  
        if (this.form.new_username.length < 5 || this.form.new_username.length > 15) {
          this.message.error = "Username must be between 5 and 15 characters.";
          return;
        }
  
        if (this.form.new_username === this.$store.state.currentUser) {
          this.message.error = "This is your current username!";
          return;
        }
  
        if (this.form.new_username !== this.form.new_confirm_username) {
          this.message.error = "Confirm username doesn't match with new username.";
          return;
        }
  
        const response = await this.azure_function("POST", "/user/get/info", { username: this.form.new_username });
        if (response?.result) {
          this.message.error = "This username has been taken.";
          return;
        }
  
        const input = {
          id: this.$store.state.currentStats.id,
          updates: { username: this.form.new_username }
        };
        const update_response = await this.azure_function("PUT", "/user/update/info", input);
  
        if (update_response?.result) {
          this.$store.commit("setCurrentUser", this.form.new_username);
          this.message.success = "Username update Successful!";
        } else {
          this.message.error = update_response?.msg || "Username update Failed.";
        }
      },
      async confirmPassword() {
        this.message = { error: "", success: "" };
  
        if (this.form.new_password.length < 8 || this.form.new_password.length > 15) {
          this.message.error = "Password must be between 8 and 15 characters.";
          return;
        }
  
        if (this.form.new_password === this.$store.state.currentPassword) {
          this.message.error = "This is your current password!";
          return;
        }
  
        if (this.form.new_password !== this.form.new_confirm_password) {
          this.message.error = "Confirm password doesn't match with new password.";
          return;
        }
  
        const input = {
          id: this.$store.state.currentStats.id,
          updates: { password: this.form.new_password }
        };
        const update_response = await this.azure_function("PUT", "/user/update/info", input);
  
        if (update_response?.result) {
          this.$store.commit("setCurrentPassword", this.form.new_password);
          this.message.success = "Password update Successful!";
        } else {
          this.message.error = update_response?.msg || "Password update Failed.";
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
      }
    }
  };
  </script>
  
  <style lang="scss" scoped>
  </style>
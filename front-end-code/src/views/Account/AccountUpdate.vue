<template>
    <div class="container">
        <h1 class="title">UPDATE DETAILS</h1>
        <div class="form-box" v-if="showChangeUsername">
            <h2>Change Username</h2>
            <button @click="next_page('main')">Back</button>
            <input type="text" placeholder="New Username" v-model="form.new_username" />
            <input type="text" placeholder="Confirm Username" v-model="form.new_confirm_username" />
            <button @click="toggleForm">Change Password</button>
            <button @click="confirmUsername">Confirm</button> 
        </div>
        <div class="form-box" v-else>
            <h2>Change Password</h2>
            <button @click="next_page('main')">Back</button>
            <input type="text" placeholder="New Password" v-model="form.new_password" />
            <input type="text" placeholder="Confirm Password" v-model="form.new_confirm_password" />
            <button @click="toggleForm">Change Username</button>
            <button @click="confirmPassword">Confirm</button> 
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
    // Page member variables and methods:
    name: "update",
    data() {
        return {
            showChangeUsername: true,
            form: {new_username: "", new_password: "", new_confirm_username: "", new_confirm_password: ""},
            message: { error: "", success: "" }
        };
    },
    methods: {
        toggleForm() {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Reset Inputs
            this.form = {new_username: "", new_password: "", new_confirm_username: "", new_confirm_password: ""};

            this.showChangeUsername = !this.showChangeUsername;
        },
        async confirmUsername() {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Check if the username has valid length.
            if (this.form.new_username.length < 5 || this.form.new_username.length > 15) {
                this.message.error = "Username must be between 5 and 15 characters.";
                return;
            }
            
            // Check if the username hasn't changed at all.
            if (this.form.new_username === this.$store.state.currentUser) {
                this.message.error = "This is your current username!";
                return;
            }
            
            // Check if the username and confirm username matches.
            if (this.form.new_username != this.form.new_confirm_username) {
                this.message.error = "Confirm username doesn't match with new username.";
                return;
            }

            // Check if this username already exists.
            const response = await this.azure_function("POST", "/user/get/info", {"username": this.form.new_username})
            if (response.result) {
                this.message.error = "This username has been taken."
                return;
            }

            // Update the username as appropriate:
            const user_stats = this.$store.state.currentStats
            const input = { 'id': user_stats.id, 'updates': { 'username': this.form.new_username } }
            const update_response = await this.azure_function("PUT", "/user/update/info", input)

            // Show message incase the API response fails, otherwise update state.
            if (update_response) {
                this.$store.commit("setCurrentUser", this.form.new_username);
                this.message.success = 'Username update Successful!'
            } else {
                this.message.error = update_response.msg || "Username update Failed."
            }
        },
        async confirmPassword() {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Check if the password has valid length.
            if (this.form.new_password.length < 8 || this.form.new_password.length > 15) {
                this.message.error = "Password must be between 8 and 15 characters.";
                return;
            }
            
            // Check if the password hasn't changed at all.
            if (this.form.new_password === this.$store.state.currentPassword) {
                this.message.error = "This is your current password!";
                return;
            }
            
            // Check if the password and confirm password matches.
            if (this.form.new_password != this.form.new_confirm_password) {
                this.message.error = "Confirm password doesn't match with new password.";
                return;
            }

            // Update the password as appropriate:
            const user_stats = this.$store.state.currentStats
            const input = { 'id': user_stats.id, 'updates': { 'password': this.form.new_password } }
            const update_response = await this.azure_function("PUT", "/user/update/info", input)

            // Show message incase the API response fails, otherwise update state.
            if (update_response) {
                this.$store.commit("setCurrentPassword", this.form.new_password);
                this.message.success = 'Password update Successful!'
            } else {
                this.message.error = update_response.msg || "Password update Failed."
            }
        },
        async azure_function(function_type, function_route, json_doc) {
        console.log("Calling API request: " + function_route + ", params: " + JSON.stringify(json_doc));
            // Call Azure function with POST request
            try {
                const url = process.env.VUE_APP_BACKEND_URL + function_route + '?code=' + process.env.VUE_APP_MASTER_KEY
                const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"},body: JSON.stringify(json_doc)});
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
    },
};
</script>

<style lang="scss" scoped>
</style>
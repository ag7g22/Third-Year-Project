<template>
    <div class="container">
        <h1 class="title">DASHBOARD | {{ logged_in_user }}</h1>
        <div class="buttons">
            <button @click="next_page('account')">Account</button>
            <button @click="load_friends_list()">Friends</button>
            <button>Daily Training</button>
            <button>Category Practice</button>
            <button>Road Sign Practice</button>
            <button @click="next_page('leaderboard')">Leaderboard</button>
            <button @click="logout()">Log out</button>   
        </div>
        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "dashboard",
    data() {
        return {
            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" }
        };
    },
    methods: {
        logout() {
            // Reset State
            this.$store.commit("setCurrentUser", "");
            this.$store.commit("setCurrentPassword", "");
            this.$store.commit("setCurrentStats", { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a'});
            console.log("Current User and Password:", this.$store.state.currentUser, this.$store.state.currentPassword);
            this.next_page('authentication')
        },
        async load_friends_list() {
            // Get API update of latest status of friends
            const friends_response = await this.azure_function("POST", "/user/friend/all", {"username": this.logged_in_user})
            if (friends_response.result) {
                this.message.success = "Retrieved Friends List! Loading Socials Page ..."

                // Update state for current friends & load next page:
                const social_lists = {friends: friends_response.msg.friends, friend_requests: friends_response.msg.friend_requests}
                this.$store.commit("setCurrentSocialLists", social_lists);
                this.next_page('friends');

            } else {
                this.message.error = friends_response.msg | "Unable to find user."
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
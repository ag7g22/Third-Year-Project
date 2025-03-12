<template>
    <div class="container">
        <h1 class="title">DASHBOARD | {{ logged_in_user }}</h1>
        <div class="buttons">
            <button @click="next_page('account')">Account</button>
            <button @click="load_friends_list()">Friends</button>
            <button>Daily Training</button>
            <button @click="next_page('lobby')">Versus</button>
            <button @click="next_page('categoryquiz')">Category Practice</button>
            <button @click="next_page('roadsignquiz')">Road Sign Practice</button>
            <button @click="next_page('hazard')">Hazard Perception</button>
            <button @click="load_leaderboards()">Leaderboard</button>
            <button @click="logout()">Log out</button>   
        </div>
        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>
  
<script>
import toastr from 'toastr';
export default {
    // Page member variables and methods:
    name: "dashboard",
    data() {
        return {
            client_socket: this.$store.state.currentClientSocket,
            logged_in_user: this.$store.state.currentUser,
            message: { error: "", success: "" },
        };
    },
    methods: {
        logout() {
            // Let server know user has logged out.
            this.client_socket.emit('logout', this.logged_in_user);

            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Reset State
            this.$store.commit("setCurrentUser", "");
            this.$store.commit("setCurrentPassword", "");
            this.$store.commit("setCurrentRank", { level: 'n/a', exp: 0, exp_threshold: 0 });
            this.$store.commit("setCurrentStats", { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a'});
            this.$store.commit("setCurrentSocialLists", {friends: [], friend_requests: []});
            console.log("Current User and Password:", this.$store.state.currentUser, this.$store.state.currentPassword);

            this.next_page('authentication');
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
                this.message.error = friends_response.msg || "Unable to find user."
            }
        },
        async load_leaderboards() {
            // Get API update of the daily leaderboard
            const leaderboard_public = await this.azure_function("GET", "/user/leaderboard", {})
            const leaderboard_friends = await this.azure_function("POST", "/user/leaderboard/friend", { "id": this.$store.state.currentStats.id })

            let public_list = [];
            let friends_list = [];

            // Update state for the current leaderboards, otherwise leave them empty.
            if (leaderboard_public.result) {
                public_list = leaderboard_public.msg; 
            }

            if (leaderboard_friends.result) {
                friends_list = leaderboard_friends.msg;
            }

            this.$store.commit("setCurrentLeaderboards", {
                public: public_list, friends: friends_list
            });
            this.next_page("leaderboard");

        },
        async add_achievement(name) {
            // Add achievement to user's achievements and notify on the UI.
            this.achievements.push(name)

            // Update database
            const input = { 'id': user_stats.id, 'updates': { 'achievements': this.achievements } }
            const update = await this.azure_function("PUT", "/user/update/info", input)
            if (update) {
                this.$store.commit("setCurrentAchievements", this.achievements);
                this.message.success = 'Achievements update Successful!'

                const options = { "closeButton": true, "debug": false, "newestOnTop": true, "progressBar": true,
                "positionClass": "toast-top-right", "preventDuplicates": true, "onclick": null, "showDuration": "300",
                "hideDuration": "1000", "timeOut": "5000", "extendedTimeOut": "1000", "showEasing": "swing",
                "hideEasing": "linear", "showMethod": "fadeIn","hideMethod": "fadeOut"}

                toastr.success('"' + `/${name}` + '""',"Achievement Unlocked:", options)
            }
        },
        async azure_function(function_type, function_route, json_doc) {
            console.log(function_route);
            // Call Azure function with request
            try {
                const url = process.env.VUE_APP_BACKEND_URL + function_route + '?code=' + process.env.VUE_APP_MASTER_KEY
                
                if (function_type === "GET") {
                    const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"} });
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                } else {
                    const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"},body: JSON.stringify(json_doc)});
                    const API_reply = await response.json();
                    console.log("Result: " + JSON.stringify(API_reply.result));
                    return API_reply
                }

            } catch (error) {
                console.error("Error:", error);
                this.message.error = "An API error occurred. Please try again later.";
            }
        },
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
</style>
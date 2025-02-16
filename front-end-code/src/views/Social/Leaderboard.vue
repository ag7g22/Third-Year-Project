<template>
    <div class="container">
        <h1 class="title">LEADERBOARD | {{ logged_in_user }}</h1>
        <div>
            <button @click="next_page('dashboard')">Back</button>
            <button @click="toggle_list('public')">Public</button>
            <button @click="toggle_list('friends')">Friends</button>
        </div>

        <!-- Conditional List Rendering -->

        <div v-if="current_list === 'public'">
            <h2>DAILY QUIZ: PUBLIC</h2>
            <ul v-if="leaderboards.public.length">
                <li v-for="(user, index) in leaderboards.public">
                    #{{ index + 1 }} {{ user.username }}: {{ user.daily_training_score }} | STREAK: {{ user.streak }}
                    <button @click="view_user(user.username)">View</button>
                </li>
            </ul>
            <div v-else> 
                <p>No users found.</p>
            </div>
        </div>

        <div v-if="current_list === 'friends'">
            <h2>DAILY QUIZ: FRIENDS</h2>
            <ul v-if="leaderboards.friends.length">
                <li v-for="(user, index) in leaderboards.friends">
                    #{{ index + 1 }} {{ user.username }}: {{ user.daily_training_score }} | STREAK: {{ user.streak }}
                    <button @click="view_user(user.username)">View</button>
                </li>
            </ul>
            <div v-else> 
                <p>You have no friends! Whats the point of a friend leaderboard if you have no friends you loser!</p>
            </div>
        </div>

    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "leaderboard",
    data() {
        return {
            current_list: "public",
            logged_in_user: this.$store.state.currentUser,
            leaderboards: this.$store.state.currentLeaderboards,
            message: { error: "", success: "" },
        };
    },
    methods: {
        toggle_list(list) {
            // Reset state
            this.message.error = "";
            this.message.success = "";
            this.current_list = list;
        },
        async view_user(username) {
            // Load up user's stats to be viewed
            const response = await this.azure_function('POST', '/user/get/info', {"username": username});
            if (response.result) { 
                // Collect the user's info
                const info = response.msg;
                const rank = info.rank;
                const stats = { id: info.id, streak: info.streak, daily_training_score: info.daily_training_score, training_completion_date: info.training_completion_date};
                const achievements = info.achievements;

                console.log("/account");
                this.$router.push({
                    path: `/account`,
                    query: { view: 'leaderboard', username: username, rank: rank, stats: stats, achievements: achievements}
                });

            } else {
                this.message.error = response.msg || "Loading user failed.";
            }
        },
        async azure_function(function_type, function_route, json_doc) {
            console.log(function_route);
            // Call Azure function with request
            try {
                const url = process.env.VUE_APP_BACKEND_URL + function_route + '?code=' + process.env.VUE_APP_MASTER_KEY
                const response = await fetch( url, { method: function_type, headers: { "Content-Type": "application/json"},body: JSON.stringify(json_doc)});
                const API_reply = await response.json();
                console.log("Result: " + JSON.stringify(API_reply.result));
                return API_reply
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
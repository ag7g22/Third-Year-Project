<template>
    <div class="container">
        <h1 class="title">SOCIAL LIST | {{ logged_in_user }}</h1>
        
        <!-- Toggle Buttons -->
        <div>
            <button @click="next_page('dashboard')">Back</button>
            <button @click="toggle_list('friends')">Friends</button>
            <button @click="toggle_list('requests')">Friend Requests</button>
            <button @click="toggle_list('search')">Search Users</button>
        </div>

        <!-- Conditional List Rendering -->
        <div v-if="current_list === 'friends'">
            <h2>Friends List</h2>
            <ul v-if="social_lists.friends.length">
                <li v-for="friend in social_lists.friends" :key="friend.id">{{ friend.username }}
                    <button @click="view_user(friend.username)"">View</button>
                    <button @click="remove_friend(friend.id, friend.username)">Remove Friend</button>
                </li>
            </ul>
        </div>

        <div v-if="current_list === 'requests'">
            <h2>Friend Requests</h2>
            <ul v-if="social_lists.friend_requests.length">
                <li v-for="request in social_lists.friend_requests" :key="request.id">
                {{ request.username }} 
                <button @click="accept_request(request.id, request.username)">Accept</button>
                <button @click="reject_request(request.id, request.username)">Decline</button>
                </li>
            </ul>
        </div>

        <div v-if="current_list === 'search'">
            <h2>Search Users</h2>
            <input type="text" id="search" v-model="search.query" placeholder="Search..." />
            <button @click="search_users" class="btn-search">🔍</button>
            <ul v-if="search.users.length">
                <li v-for="user in search.users" :key="user.id">
                {{ user.username }}
                <button @click="view_user(user.username)"">View</button>
                <button v-if="!social_lists.friends.some(friend => friend.username === user.username)" @click="send_friend_request(user.id)">Add Friend</button>
                </li>
            </ul>
        </div>

        <p v-if="message.error" class="error-message">{{ message.error }}</p>
        <p v-else-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "friends",
    mounted() {
        this.current_list = this.$route.query.current_list || "friends";
        this.search = this.$route.query.search || { query: "", users: [] };
    },
    data() {
        return {
            // Default view
            current_list: "friends",
            search: { query: "", users: [] },
            logged_in_user: this.$store.state.currentUser,
            stats: this.$store.state.currentStats,
            social_lists: this.$store.state.currentSocialLists,
            message: { error: "", success: "" }
        };
    },
    methods: {
        toggle_list(list) {
            // Reset state
            this.message.error = "";
            this.message.success = "";
            this.search = { query: "", users: [] };

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
                    query: { view: 'user', username: username, rank: rank, stats: stats, achievements: achievements,
                    current_list: this.current_list, search: this.search  }
                });

            } else {
                this.message.error = response.msg || "Loading user failed.";
            }
        },
        async remove_friend(id, username) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Remove both friends:
            const input = {"id_1": this.stats.id, "id_2": id}
            const remove = await this.azure_function("POST", "/user/friend/remove", input)
            if (remove.result) {
                this.message.success = 'Removed friend!'
                
                // Remove from the friends list
                let friends = this.social_lists.friends;
                let friend_requests = this.social_lists.friend_requests;
                friends = friends.filter(friend => (friend.id !== id, friend.username !== username))

                console.log('Friends:', friends)

                this.$store.commit("setCurrentSocialLists", {friends: friends, friend_requests: friend_requests});
                this.social_lists = {friends: friends, friend_requests: friend_requests}

            } else {
                this.message.error = accept.msg || "Friend removal Failed."
            }
        },
        async accept_request(id, username) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Accept the friend request:
            const input = {"sender_id": this.stats.id, "recipient_id": id};
            const accept = await this.azure_function("POST", "/user/friend/accept", input)
            if (accept.result) {
                this.message.success = 'Accepted request!';

                // Remove from the friend request list and add to friend list
                let friends = this.social_lists.friends;
                let friend_requests = this.social_lists.friend_requests;
                friend_requests = friend_requests.filter(friend => (friend.id !== id, friend.username !== username))
                friends.push({'id': id, 'username': username})

                console.log('Friend requests:', friend_requests)
                console.log('Friends:', friends)
                
                this.$store.commit("setCurrentSocialLists", {friends: friends, friend_requests: friend_requests});
                this.social_lists = {friends: friends, friend_requests: friend_requests}
            } else {
                this.message.error = accept.msg || "Friend accept Failed."
            }
        },
        async reject_request(id, username) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Reject the friend request:
            const input = {"sender_id": id, "sender_username": username, "recipient_id": this.stats.id};
            const reject = await this.azure_function("POST", "/user/friend/reject", input)
            if (reject.result) {
                this.message.success = 'Rejected request!';

                // Remove from friend request list ONLY
                let friends = this.social_lists.friends;
                let friend_requests = this.social_lists.friend_requests;
                friend_requests = friend_requests.filter((friend => (friend.id !== id, friend.username !== username)))

                console.log('Friend requests:', friend_requests)
                
                this.$store.commit("setCurrentSocialLists", {friends: friends, friend_requests: friend_requests});
                this.social_lists = {friends: friends, friend_requests: friend_requests}

            } else {
                this.message.error = reject.msg || "Friend reject Failed."
            }
        },
        async send_friend_request(recipient_id) {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Send the friend request:
            const input = {"sender_id": this.stats.id, "sender_username": this.logged_in_user, "recipient_id": recipient_id};
            const search = await this.azure_function("POST", "/user/friend/request", input)
            if (search.result) {
                this.message.success = 'Sent request!';
            } else {
                this.message.error = search.msg || "Friend request Failed."
            }
        },
        async search_users() {
            // Reset messages
            this.message.error = "";
            this.message.success = "";

            // Check if the username is the same as the logged in user.
            if (this.search.query === this.$store.state.currentUser) {
                this.message.error = "This is you!";
                return;
            }
            
            // Search for users in the API:
            const search = await this.azure_function("POST", "/user/search", {"username": this.logged_in_user, "search": this.search.query})
            if (search.result) {
                this.message.success = 'Found users!'
                // Populate the search queries
                this.search.users = search.msg
            } else {
                this.message.error = search.msg || "Username search Failed."
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
            // Move onto either dashboard or friend account page:
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
</style>
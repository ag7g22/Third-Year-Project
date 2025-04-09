<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')">🎲 Dashboard</button>
        <button @click="next_page('account')">👤 Account</button>
        <button disabled>👥 Friends</button>
        <button @click="load_leaderboards">🏆 Leaderboard</button>
        <button @click="logout">🔒 Log out</button> 
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <h1 class="title">SOCIAL LIST | {{ logged_in_user }}</h1>
  
      <!-- Toggle Buttons -->
      <div>
        <button @click="toggle_list('friends')">Friends</button>
        <button @click="toggle_list('requests')">Friend Requests</button>
        <button @click="toggle_list('search')">Search Users</button>
      </div>
  
      <!-- Friends List -->
      <div v-if="current_list === 'friends'">
        <h2>Friends List</h2>
        <ul v-if="social_lists.friends.length">
          <li v-for="friend in social_lists.friends" :key="friend.id">
            {{ friend.username }}
            <button @click="view_user(friend.username)">View</button>
            <button @click="remove_friend(friend.id, friend.username)">Remove Friend</button>
          </li>
        </ul>
      </div>
  
      <!-- Friend Requests -->
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
  
      <!-- Search Users -->
      <div v-if="current_list === 'search'">
        <h2>Search Users</h2>
        <input type="text" v-model="search.query" placeholder="Search..." />
        <button @click="search_users">🔍</button>
        <ul v-if="search.users.length">
          <li v-for="user in search.users" :key="user.id">
            {{ user.username }}
            <button @click="view_user(user.username)">View</button>
            <button v-if="!is_friend(user.username)" @click="send_friend_request(user.id, user.username)">Add Friend</button>
          </li>
        </ul>
      </div>
  
      <p v-if="message.error" class="error-message">{{ message.error }}</p>
      <p v-else-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
  </div>
</template>

<script>
import toastr from 'toastr';
import 'toastr/build/toastr.min.css';

export default {
  name: "friends",
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      current_list: this.$route.query.current_list || "friends",
      search: this.$route.query.search || { query: "", users: [] },
      logged_in_user: this.$store.state.currentUser,
      stats: this.$store.state.currentStats,
      social_lists: this.$store.state.currentSocialLists,
      message: { error: "", success: "" }
    };
  },
  methods: {
    clearMessages() {
      this.message.error = "";
      this.message.success = "";
    },
    toggle_list(list) {
      this.message = { error: "", success: "" };
      this.search = { query: "", users: [] };
      this.current_list = list;
    },
    is_friend(username) {
      return this.social_lists.friends.some(friend => friend.username === username);
    },
    async view_user(username) {
      const response = await this.azure_function('POST', '/user/get/info', { username });
      if (response.result) {
        const info = response.msg;
        const routeData = {
          path: '/account',
          query: {
            view: 'friends_list',
            username,
            rank: info.rank,
            stats: {
              id: info.id,
              streak: info.streak,
              daily_training_score: info.daily_training_score,
              training_completion_date: info.training_completion_date
            },
            achievements: info.achievements,
            current_list: this.current_list,
            search: this.search
          }
        };
        this.$router.push(routeData);
      } else {
        this.message.error = response.msg || "Loading user failed.";
      }
    },
    async remove_friend(id, username) {
      this.reset_messages();
      const input = { id_1: this.stats.id, id_2: id };
      const response = await this.azure_function("POST", "/user/friend/remove", input);
      if (response.result) {
        this.message.success = 'Removed friend!';
        const friends = this.social_lists.friends.filter(friend => friend.id !== id);
        this.update_social_lists(friends, this.social_lists.friend_requests);
      } else {
        this.message.error = response.msg || "Friend removal Failed.";
      }
    },
    async accept_request(id, username) {
      this.reset_messages();
      const input = { sender_id: this.stats.id, recipient_id: id };
      const response = await this.azure_function("POST", "/user/friend/accept", input);
      if (response.result) {
        this.message.success = 'Accepted request!';
        const friend_requests = this.social_lists.friend_requests.filter(r => r.id !== id);
        const friends = [...this.social_lists.friends, { id, username }];
        this.update_social_lists(friends, friend_requests);
      } else {
        this.message.error = response.msg || "Friend accept Failed.";
      }
    },
    async reject_request(id, username) {
      this.reset_messages();
      const input = { sender_id: id, sender_username: username, recipient_id: this.stats.id };
      const response = await this.azure_function("POST", "/user/friend/reject", input);
      if (response.result) {
        this.message.success = 'Rejected request!';
        const friend_requests = this.social_lists.friend_requests.filter(r => r.id !== id);
        this.update_social_lists(this.social_lists.friends, friend_requests);
      } else {
        this.message.error = response.msg || "Friend reject Failed.";
      }
    },
    async send_friend_request(recipient_id, recipient_username) {
      this.reset_messages();
      const input = { sender_id: this.stats.id, sender_username: this.logged_in_user, recipient_id };
      const response = await this.azure_function("POST", "/user/friend/request", input);
      if (response.result) {
        this.message.success = 'Sent request!';
        toastr.success(`Sent friend request to "${recipient_username}"`, {
          closeButton: true,
          progressBar: true,
          timeOut: 5000,
          positionClass: "toast-top-right"
        });
      } else {
        this.message.error = response.msg || "Friend request Failed.";
      }
    },
    async search_users() {
      this.reset_messages();
      if (this.search.query === this.logged_in_user) {
        this.message.error = "This is you!";
        return;
      }
      const response = await this.azure_function("POST", "/user/search", {
        username: this.logged_in_user,
        search: this.search.query
      });
      if (response.result) {
        this.message.success = 'Found users!';
        this.search.users = response.msg;
      } else {
        this.message.error = response.msg || "Username search Failed.";
      }
    },
    async azure_function(method, route, data) {
      try {
          console.log(route);
        const url = `${process.env.VUE_APP_BACKEND_URL}${route}?code=${process.env.VUE_APP_MASTER_KEY}`;
        const response = await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        return await response.json();
      } catch (error) {
        console.error("Azure Function Error:", error);
        this.message.error = "An API error occurred. Please try again later.";
      }
    },
    update_social_lists(friends, friend_requests) {
      this.$store.commit("setCurrentSocialLists", { friends, friend_requests });
      this.social_lists = { friends, friend_requests };
    },
    reset_messages() {
      this.message = { error: "", success: "" };
    },
    logout() {
      this.client_socket.emit('logout', this.logged_in_user);
      this.clearMessages();

      // Reset state
      this.$store.commit("setCurrentUser", "");
      this.$store.commit("setCurrentPassword", "");
      this.$store.commit("setCurrentRank", { level: 'n/a', exp: 0, exp_threshold: 0 });
      this.$store.commit("setCurrentStats", { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a' });
      this.$store.commit("setCurrentSocialLists", { friends: [], friend_requests: [] });
      console.log("User logged out.");

      this.next_page('authentication');
    },
  async load_leaderboards() {
    const [publicRes, friendsRes] = await Promise.all([
      this.azure_function("GET", "/user/leaderboard", {}),
      this.azure_function("POST", "/user/leaderboard/friend", { id: this.$store.state.currentStats.id })
    ]);

    this.$store.commit("setCurrentLeaderboards", {
      public: publicRes.result ? publicRes.msg : [],
      friends: friendsRes.result ? friendsRes.msg : []
    });

    this.next_page("leaderboard");
  },
  async add_achievement(name) {
    this.achievements.push(name);
    const userId = this.$store.state.currentStats.id;
    const input = { id: userId, updates: { achievements: this.achievements } };
    const update = await this.azure_function("PUT", "/user/update/info", input);

    if (update) {
      this.$store.commit("setCurrentAchievements", this.achievements);
      this.message.success = 'Achievements update Successful!';

      toastr.success(`"${name}"`, "Achievement Unlocked:", {
        closeButton: true, progressBar: true, positionClass: "toast-top-right",
        showDuration: "300", hideDuration: "1000", timeOut: "5000",
        extendedTimeOut: "1000", showEasing: "swing", hideEasing: "linear",
        showMethod: "fadeIn", hideMethod: "fadeOut"
      });
    }
  },
  async azure_function(method, route, body) {
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
      console.log("Result: ", JSON.stringify(result.result));
      return result;
    } catch (error) {
      console.error("Error:", error);
      this.message.error = "An API error occurred. Please try again later.";
    }
  },
  next_page(page) {
    console.log("/" + page);
    this.$router.push(`/${page}`);
  }
  }
};
</script>

<style lang="scss" scoped>
</style>
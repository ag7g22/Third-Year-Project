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

      <!-- Friends List -->
      <div v-if="current_list === 'friends'">
        <div class="list-container">
          <h2>Friends List</h2>
          <ul v-if="social_lists.friends.length" class="user-list">
            <li v-for="friend in social_lists.friends" :key="friend.id" class="user-card">
              <div class="username">{{ friend.username }}</div>
              <div class="user-actions">
                <button @click="view_user(friend.username)">View</button>
                <button @click="remove_friend(friend.id, friend.username)">Remove Friend</button>
              </div>
            </li>
          </ul>
          <h3 v-else>"I work alone" ahh list 💀</h3>
        </div>
        <div class="game-buttons">
          <button class="game-button" disabled>Friends</button>
          <button class="game-button" @click="toggle_list('requests')">Friend Requests</button>
          <button class="game-button" @click="toggle_list('search')">Search Users</button>
        </div>
      </div>
  
      <!-- Friend Requests -->
      <div v-if="current_list === 'requests'">
        <div class="list-container">
          <h2>Friend Requests</h2>
          <ul v-if="social_lists.friend_requests.length" class="user-list">
            <li v-for="request in social_lists.friend_requests" :key="request.id" class="user-card">
              <div class="username">{{ request.username }}</div>
              <div class="user-actions">
                <button @click="accept_request(request.id, request.username)">Accept</button>
                <button @click="reject_request(request.id, request.username)">Decline</button>
              </div>
            </li>
          </ul>
          <h3 v-else>*cricket noises*</h3>
        </div>
        <div class="game-buttons">
          <button class="game-button" @click="toggle_list('friends')">Friends</button>
          <button class="game-button" disabled>Friend Requests</button>
          <button class="game-button" @click="toggle_list('search')">Search Users</button>
        </div>
      </div>
  
      <!-- Search Users -->
      <div v-if="current_list === 'search'">
        <div class="list-container">
          <h2>Search Users</h2>
          <div class="search-bar">
            <input type="text" v-model="search.query" placeholder="Search..." />
            <button @click="search_users">🔍</button>
          </div>
          
          <ul v-if="search.users.length" class="user-list">
            <li v-for="user in search.users" :key="user.id" class="user-card">
              <div class="username">{{ user.username }}</div>
              <div class="user-actions">
                <button @click="view_user(user.username)">View</button>
                <button 
                  v-if="!is_friend(user.username)" 
                  @click="send_friend_request(user.id, user.username)">
                  Add Friend
                </button>
              </div>
            </li>
          </ul>
          <h3 v-else>Lets find you some friends eh?</h3>
        </div>
        <div class="game-buttons">
          <button class="game-button" @click="toggle_list('friends')">Friends</button>
          <button class="game-button" @click="toggle_list('requests')">Friend Requests</button>
          <button class="game-button" disabled>Search Users</button>
        </div>
      </div>
  
      <p v-if="message.error" class="error-message">{{ message.error }}</p>
      <p v-else-if="message.success" class="success-message">{{ message.success }}</p>
    </div>
  </div>
</template>

<script>
import toastr from 'toastr';
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
    info_message(title, msg) {
      toastr.info(msg, title, {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-top-right",
          timeOut: 5000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut",
          preventDuplicates: false
      });
    },
    successful_message(title, msg) {
        toastr.success(msg, title, {
        closeButton: true,
        progressBar: true,
        positionClass: "toast-top-right",
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
        positionClass: "toast-top-right",
        timeOut: 5000,
        showMethod: "fadeIn",
        hideMethod: "fadeOut",
        preventDuplicates: true
        });
    },
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
            recent_category_scores: info.recent_category_scores,
            current_list: this.current_list,
            search: this.search
          }
        };
        this.$router.push(routeData);
      } else {
        this.error_message('Loading user failed!', ' ');
      }
    },
    async remove_friend(id, username) {
      this.reset_messages();
      const input = { id_1: this.stats.id, id_2: id };
      const response = await this.azure_function("POST", "/user/friend/remove", input);
      if (response.result) {
        this.add_achievement('A sworn enemy','💔');
        this.successful_message('Removed friend:', username);
        const friends = this.social_lists.friends.filter(friend => friend.id !== id);
        this.update_social_lists(friends, this.social_lists.friend_requests);
      } else {
        this.error_message('Failed!', response.msg);
      }
    },
    async accept_request(id, username) {
      this.reset_messages();
      const input = { sender_id: this.stats.id, recipient_id: id };
      const response = await this.azure_function("POST", "/user/friend/accept", input);
      if (response.result) {
        this.add_achievement('A remarkable ally','🤝');
        this.successful_message('Added friend:', username);
        const friend_requests = this.social_lists.friend_requests.filter(r => r.id !== id);
        const friends = [...this.social_lists.friends, { id, username }];
        this.update_social_lists(friends, friend_requests);
      } else {
        this.error_message('Failed!', response.msg);
      }
    },
    async reject_request(id, username) {
      this.reset_messages();
      const input = { sender_id: id, sender_username: username, recipient_id: this.stats.id };
      const response = await this.azure_function("POST", "/user/friend/reject", input);
      if (response.result) {
        this.successful_message('Rejected user:', username);
        const friend_requests = this.social_lists.friend_requests.filter(r => r.id !== id);
        this.update_social_lists(this.social_lists.friends, friend_requests);
      } else {
        this.error_message('Failed!', response.msg);
      }
    },
    async send_friend_request(recipient_id, recipient_username) {
      this.reset_messages();
      const input = { sender_id: this.stats.id, sender_username: this.logged_in_user, recipient_id };
      const response = await this.azure_function("POST", "/user/friend/request", input);
      if (response.result) {
        this.add_achievement('Request for alliance','📨');
        this.info_message('Sent request to user:', recipient_username);
      } else {
        this.error_message('Failed!', response.msg);
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
        this.successful_message('Found users!', ' ');
        this.search.users = response.msg;
      } else {
        this.error_message('No users found.', ' ');
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
  async add_achievement(name, emoji) {
      // Add an achievement in the user's data!
      if (this.$store.state.currentAchievements.includes(name)) {
          console.log("Already gotten the " + name + " achievement!")
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
.search-bar {
  display: flex;
  align-items: center; /* ensures vertical alignment */
  gap: 10px; /* space between input and button */
}

.search-bar input {
  flex: 1; /* allow input to grow */
  padding: 10px;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #f3af59;
  background-color: rgb(20, 20, 20);
  height: 40px; /* consistent height */
}

.search-bar button {
  height: 40px; /* match input height */
  padding: 10px 15px;
  font-size: 1rem;
  border-radius: 6px;
  background-color: #f3af59;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
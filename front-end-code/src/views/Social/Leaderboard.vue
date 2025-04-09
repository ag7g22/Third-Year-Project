<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')">🎲 Dashboard</button>
        <button @click="next_page('account')">👤 Account</button>
        <button @click="load_friends_list">👥 Friends</button>
        <button disabled>🏆 Leaderboard</button>
        <button @click="logout">🔒 Log out</button> 
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="main-content">
      <h1 class="title">LEADERBOARD | {{ logged_in_user }}</h1>
      <div>
        <button @click="next_page('dashboard')">Back</button>
        <button @click="toggle_list('public')">Public</button>
        <button @click="toggle_list('friends')">Friends</button>
      </div>
  
      <!-- Leaderboard Sections -->
      <div v-if="current_list === 'public'">
        <h2>DAILY QUIZ: PUBLIC</h2>
        <ul v-if="leaderboards?.public?.length">
          <li v-for="(user, index) in leaderboards.public" :key="user.username">
            #{{ index + 1 }} {{ user.username }}: {{ user.daily_training_score }} | STREAK: {{ user.streak }}
            <button @click="view_user(user.username)">View</button>
          </li>
        </ul>
        <p v-else>No users found.</p>
      </div>
  
      <div v-else-if="current_list === 'friends'">
        <h2>DAILY QUIZ: FRIENDS</h2>
        <ul v-if="leaderboards?.friends?.length">
          <li v-for="(user, index) in leaderboards.friends" :key="user.username">
            #{{ index + 1 }} {{ user.username }}: {{ user.daily_training_score }} | STREAK: {{ user.streak }}
            <button @click="view_user(user.username)">View</button>
          </li>
        </ul>
        <p v-else>You have no friends! What's the point of a friend leaderboard if you have no friends, you loser!</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "leaderboard",
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      current_list: "public",
      logged_in_user: this.$store.state.currentUser,
      leaderboards: this.$store.state.currentLeaderboards,
      message: { error: "", success: "" },
    };
  },
  methods: {
    clearMessages() {
      this.message.error = "";
      this.message.success = "";
    },
    toggle_list(list) {
      this.message = { error: "", success: "" };
      this.current_list = list;
    },
    async view_user(username) {
      const response = await this.azure_function("POST", "/user/get/info", { username });
      if (response?.result) {
        const { id, streak, daily_training_score, training_completion_date, achievements, rank } = response.msg;

        this.$router.push({
          path: "/account",
          query: {
            view: "leaderboard",
            username,
            rank,
            stats: { id, streak, daily_training_score, training_completion_date },
            achievements,
          },
        });
      } else {
        this.message.error = response?.msg || "Loading user failed.";
      }
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
    async load_friends_list() {
      const response = await this.azure_function("POST", "/user/friend/all", { username: this.logged_in_user });

      if (response.result) {
        this.message.success = "Retrieved Friends List! Loading Socials Page ...";
        this.$store.commit("setCurrentSocialLists", {
          friends: response.msg.friends,
          friend_requests: response.msg.friend_requests
        });
        this.next_page('friends');
      } else {
        this.message.error = response.msg || "Unable to find user.";
      }
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
  },
  },
};
</script>

<style lang="scss" scoped>
</style>
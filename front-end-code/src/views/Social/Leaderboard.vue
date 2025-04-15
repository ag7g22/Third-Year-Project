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
  
      <!-- Leaderboard Sections -->
      <div v-if="current_list === 'public'">
        <div class="list-container">
          <h2>PUBLIC</h2>
          <ul v-if="leaderboards?.public?.length" class="user-list">
            <li
              v-for="(user, index) in leaderboards.public"
              :key="user.username"
              :class="['user-card', 
                        { gold: index === 0, silver: index === 1, bronze: index === 2 }]">
              <div v-if="index === 0">
                <div class="username">#{{ index + 1 }} {{ user.username }} 👑</div>
              </div>
              <div v-else>
                <div class="username">#{{ index + 1 }} {{ user.username }}</div>
              </div>
              <div class="user-actions">
                <h3>{{ user.daily_training_score }}</h3>
                <h3>🔥{{ user.streak }}</h3>
                <button @click="view_user(user.username)">View</button>
              </div>
            </li>
          </ul>
          <h3 v-else>Damn, no one has done the daily quiz yet. Bunch of procrasinators</h3>
        </div>
        <div class="game-buttons">
          <button class="game-button" disabled>Public</button>
          <button class="game-button" @click="toggle_list('friends')">Friends</button>
        </div>
      </div>
  
      <div v-else-if="current_list === 'friends'">
        <div class="list-container">
          <h2>FRIENDS</h2>
          <ul v-if="leaderboards?.friends?.length" class="user-list">
            <li
              v-for="(user, index) in leaderboards.friends"
              :key="user.username"
              :class="['user-card', 
                        { gold: index === 0, silver: index === 1, bronze: index === 2 }]">
              <div v-if="index === 0">
                <div class="username">#{{ index + 1 }} {{ user.username }} 👑</div>
              </div>
              <div v-else>
                <div class="username">#{{ index + 1 }} {{ user.username }}</div>
              </div>
              <div class="user-actions">
                <h3>{{ user.daily_training_score }}</h3>
                <h3>🔥{{ user.streak }}</h3>
                <button @click="view_user(user.username)">View</button>
              </div>
            </li>
          </ul>
          <h3 v-else>You have no friends! What's the point of a friend leaderboard if you have no friends, you loser!</h3>
        </div>
        <div class="game-buttons">
          <button class="game-button" @click="toggle_list('public')">Public</button>
          <button class="game-button" disabled>Friends</button>
        </div>
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
        const { id, streak, daily_training_score, training_completion_date, achievements, rank, recent_category_scores } = response.msg;

        this.$router.push({
          path: "/account",
          query: {
            view: "leaderboard",
            username,
            rank,
            stats: { id, streak, daily_training_score, training_completion_date },
            achievements,
            recent_category_scores,
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
.user-card.gold {
  border: 2px solid #ffd700;
  color: #eadfa1;
}

.user-card.gold button {
  color: #eadfa1;
}

.user-card.silver {
  border: 2px solid #c0c0c0;
  color: #d6d5d5;
}

.user-card.user-card.silver button {
  color: #d6d5d5;
}

.user-card.bronze {
  border: 2px solid #cd7f32;
  color: #fcad5d;
}

.user-card.user-card.bronze button {
  color: #fcad5d;
}
</style>
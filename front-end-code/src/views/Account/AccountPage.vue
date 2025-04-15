<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div v-if="this.view === 'friends_list'" class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button @click="next_page('account')"> 👤 Account</button>
        <button disabled> 👥 Friends</button>
        <button @click="load_leaderboards"> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
      </div>
    </div>
    <div v-else-if="this.view === 'leaderboard'" class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button @click="next_page('account')"> 👤 Account</button>
        <button @click="load_friends_list"> 👥 Friends</button>
        <button disabled> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
      </div>
    </div>
    <div v-else class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button disabled> 👤 Account</button>
        <button @click="load_friends_list"> 👥 Friends</button>
        <button @click="load_leaderboards"> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">

      <div class="list-container">
      <!-- Top: Username and EXP Bar -->
      <div class="profile-header">
        <h2 class="username">🔥{{ stats.streak }} {{ username }}</h2>
        <p class="level">LVL. {{ rank.level }}</p>
      </div>

      <div class="exp-bar-container">
        <div class="exp-bar-fill" :style="{ width: ((rank.exp / rank.exp_threshold) * 100) + '%' }"></div>
      </div>
      <p class="exp-label">EXP: {{ rank.exp }} / {{ rank.exp_threshold }}</p>

        <div class="profile-content">
          <!-- Left: User Stats -->
          <div class="user-stats">
            <p>ID: {{ stats.id }}</p>
            <p>Daily Score: {{ stats.daily_training_score }}</p>
            <p>Daily Completed: {{ stats.training_completion_date }}</p>
          </div>

          <!-- Right: Achievements -->
          <div class="achievements-box" v-if="user_achievements.length">
            <h3>Achievements</h3>
            <ul>
              <li v-for="achievement in user_achievements" :key="achievement.name">
                {{ achievement.name }} - {{ achievement.description }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Bottom: Graph Box -->
        <div class="graph-box">
          <div class="score-row" v-for="(score, topic) in progress_scores" :key="topic">
            <div class="label">{{ topic }}</div>
            <div class="bar-container">
              <div class="bar"
                  :style="{ width: (score * 100) + '%', backgroundColor: colorMap[topic] }">
              </div>
            </div>
            <div class="value">{{ (score * 100).toFixed(0) }}%</div>
          </div>
        </div>
      </div>

      <!-- Buttons -->
      <div v-if="view !== 'logged_user'">
        <div class="game-buttons">
          <button class="game-button" @click="handleBack">Return</button> 
        </div>
      </div>
      <div v-else>
        <div class="game-buttons">
          <button class="game-button">Toggle graph</button> 
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "account",
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      logged_in_user: this.$store.state.currentUser,
      view: this.$route.query.view || 'logged_user',
      username: this.$route.query.username || this.$store.state.currentUser,
      rank: this.$route.query.rank || this.$store.state.currentRank,
      stats: this.$route.query.stats || this.$store.state.currentStats,
      achievements: this.$route.query.achievements || this.$store.state.currentAchievements,
      recent_category_scores: this.$store.state.recent_category_scores || this.$store.state.currentRecentCatScores,
      current_list: this.$route.query.current_list || "friends",
      search: this.$route.query.search || { query: "", users: [] },
      achievementsWithDescriptions: [
        { name: 'Start of a Journey', description: 'Unlocked after logging in for the first time.' },
        { name: 'Gearin up', description: 'Done a daily quiz for the first time.' },
        { name: 'Levelin up', description: 'Reached level 10 for the first time.' },
        { name: 'Gear 2nd', description: 'Reached a streak of 10' },
        { name: 'Gear 3rd', description: 'Reached a streak of 50' },
        { name: 'Gear 4th', description: 'Reached a streak of 100' },
        { name: 'Gear 5th', description: 'Reached a streak of 500' },
      ],
      colorMap: {
                "Driving Off": "#4caf50",         // green
                "Urban Driving": "#2196f3",       // blue
                "Rural Driving": "#9c27b0",       // purple
                "Bigger Roads": "#ff9800",        // orange
                "Motorways": "#f44336",           // red
                "Tricky Conditions": "#ffc107",   // amber
                "Breakdowns": "#795548",          // brown
      },
      message: { error: "", success: "" }
    };
  },
  computed: {
    user_achievements() {
      return this.achievements.map(name => {
        const match = this.achievementsWithDescriptions.find(a => a.name === name);
        return match || { name, description: 'No description available' };
      });
    },
    progress_scores() {
      const scores = {};
      console.log(this.recent_category_scores);
      for (const category in this.recent_category_scores) {
        const values = this.recent_category_scores[category];
        const sum = values.reduce((acc, val) => acc + val, 0);
        scores[category] = parseFloat((sum / 10).toFixed(2));
      }
      return scores;
    }
  },
  methods: {
    clearMessages() {
      this.message.error = "";
      this.message.success = "";
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
    },
    handleBack() {
      const pageMap = {
        friends_list: {
          path: '/friends',
          query: { current_list: this.current_list, search: this.search }
        },
        leaderboard: { path: '/leaderboard' },
        logged_user: { path: '/dashboard' }
      };
      const route = pageMap[this.view] || { path: '/dashboard' };
      this.$router.push(route);
    }
  }
};
</script>

<style lang="scss" scoped>
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.username {
  font-size: 24px;
  font-weight: bold;
  color: white;
  margin: 0;
}

.level {
  font-size: 20px;
  font-weight: bold;
  color: #f3af59;
  margin: 0;
}

.exp-bar-container {
  width: 100%;
  height: 10px;
  background-color: #333;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 5px;
}

.exp-bar-fill {
  height: 100%;
  background-color: #079cb0;
  transition: width 0.3s ease-in-out;
}

.profile-content {
  display: flex;
  justify-content: space-between;
  gap: 40px;
  margin-bottom: 30px;
}

.user-stats {
  color: #f3af59;
  flex: 1;
  text-align: left;
  justify-content: center;
  gap: 20px;
}

.achievements-box {
  flex: 2;
}

.achievements-box ul {
  padding-left: 20px;
}
</style>
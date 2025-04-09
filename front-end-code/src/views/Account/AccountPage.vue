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
      <h1 class="title">ACCOUNT | {{ username }}</h1>
  
      <!-- User Stats -->
      <div>
        <div>
          <p>ID: {{ stats.id }}</p>
          <p>LEVEL {{ rank.level }}</p>
          <p>EXP: {{ rank.exp }} / {{ rank.exp_threshold }}</p>
          <p>STREAK: {{ stats.streak }}</p>
          <p>Daily Score: {{ stats.daily_training_score }}</p>
          <p>Daily Quiz Completed: {{ stats.training_completion_date }}</p>
        </div>
      </div>
  
      <!-- Achievements Box -->
      <div v-if="user_achievements.length" class="achievements-box">
        <h3>Achievements</h3>
        <ul>
          <li v-for="achievement in user_achievements" :key="achievement.name">
            {{ achievement.name }} - {{ achievement.description }}
          </li>
        </ul>
      </div>
      <div v-if="view !== 'logged_user'">
        <button @click="handleBack">Return</button> 
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
      current_list: this.$route.query.current_list || "friends",
      search: this.$route.query.search || { query: "", users: [] },
      achievementsWithDescriptions: [
        { name: 'Hello World!', description: 'Unlocked after logging in for the first time.' },
        { name: 'Start of a Journey', description: 'Done a daily quiz for the first time.' },
        { name: 'Levelin up', description: 'Reached level 10 for the first time.' },
        { name: 'Gear 2nd', description: 'Reached a streak of 10' },
        { name: 'Gear 3rd', description: 'Reached a streak of 50' },
        { name: 'Gear 4th', description: 'Reached a streak of 100' },
        { name: 'Gear 5th', description: 'Reached a streak of 500' },
      ],
      message: { error: "", success: "" }
    };
  },
  computed: {
    user_achievements() {
      return this.achievements.map(name => {
        const match = this.achievementsWithDescriptions.find(a => a.name === name);
        return match || { name, description: 'No description available' };
      });
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
</style>
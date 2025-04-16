<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button disabled>🎲 Dashboard</button>
        <button @click="next_page('account')">👤 Account</button>
        <button @click="load_friends_list">👥 Social Hub</button>
        <button @click="load_leaderboards">🏆 Leaderboard</button>
        <button @click="logout">🔒 Log out</button> 
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="progress-container">
        <div class="progress-title-row">
          <span class="progress-title">Exam-ready level:</span>
          <span class="progress-percent">{{ progressBarWidth }}%</span>
        </div>
        <div class="exam-ready-wrapper">
          <div class="exam-ready-bar" :style="{ width: progressBarWidth + '%' }"></div>
        </div>
      </div>
      <div class="buttons-grid">
        <button @click="next_page('dailyquiz')">
          <img src="@/assets/titles/DailyQuiz.png" alt="Logo"/>
        </button>
        <button @click="next_page('categoryquiz')">
          <img src="@/assets/titles/CategoryQuiz.png" alt="Logo"/>
        </button>
        <button @click="next_page('roadsignquiz')">
          <img src="@/assets/titles/RoadSign.png" alt="Logo"/>
        </button>
        <button @click="next_page('hazard')">
          <img src="@/assets/titles/HazardPerception.png" alt="Logo"/>
        </button>
        <button @click="next_page('lobby')">
          <img src="@/assets/titles/CrashQuizOff.png" alt="Logo"/>
        </button>
        <button @click="next_page('mockexam')">
          <img src="@/assets/titles/MockTest.png" alt="Logo"/>
        </button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "dashboard",
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      logged_in_user: this.$store.state.currentUser,
      message: { error: "", success: "" },
      achievements: this.$store.state.currentAchievements,
    };
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
  computed: {
        progressBarWidth() {
          const averages = {};

          // Calculate average for each category
          for (const category in this.$store.state.currentRecentCatScores) {
            const scores = this.$store.state.currentRecentCatScores[category];
            const sum = scores.reduce((acc, score) => acc + score, 0);
            averages[category] = (sum / scores.length).toFixed(3);  // Round to 3 decimal places
          }

          // Calculate the average of the averages
          const avgOfAverages = (
            Object.values(averages).reduce((acc, avg) => acc + parseFloat(avg), 0) / Object.values(averages).length
          ).toFixed(3);

          const percentage = parseFloat(avgOfAverages) * 100;

          // Return 0 if it's zero (or a falsey value), otherwise return the number
          return percentage || 0;
    }
  },
};
</script>

<style lang="scss" scoped>
.main-content h1 {
  color: #f3af59; /* Set the text color to the original color */
  padding: 40px;
  text-decoration: underline;
}

.main-content img {
  width: 280px;
}

.buttons-grid {
  padding: 30px;
  width: 90%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  place-items: center;
  margin: 0 auto; /* centers the grid horizontally */
}

.buttons-grid button {
  width: 90%;
  height: 200px;
  background: none;
  background-size: cover; /* Make sure the image covers the entire button */
  background-position: center; /* Center the image */
  border: none; /* Remove any border */
  cursor: pointer; /* Make the cursor a pointer to indicate it's clickable */
  transition: transform 0.3s ease; /* Smooth transition for the scale effect */
}

.buttons-grid button:hover {
  transform: scale(1.2); /* Grow the button when hovering */
}

.progress-container {
  width: 90%;
  margin: 20px auto;
}

.progress-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-title {
  color: #079cb0;
  font-size: 18px;
  font-weight: bold;
}

.progress-percent {
  font-size: 16px;
  font-weight: bold;
  color: #079cb0;
}

.exam-ready-wrapper {
  width: 100%;
  height: 20px;
  background-color: #000;
  border-radius: 10px;
  overflow: hidden;
}

.exam-ready-bar {
  height: 100%;
  background-color: #079cb0;
  transition: width 0.5s ease-in-out;
}

</style>
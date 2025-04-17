<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button disabled>🎲 Dashboard</button>
        <button @click="next_page('account')"> 👤 Account</button>
        <button @click="load_friends_list"> 👥 Social Hub</button>
        <button @click="load_leaderboards"> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="progress-container">
        <div class="progress-title-row">
          <span class="progress-title">Exam-ready level:</span>
          <span class="progress-percent">{{ progress_bar_width }}%</span>
        </div>
        <div class="exam-ready-wrapper">
          <div class="exam-ready-bar" :style="{ width: progress_bar_width + '%' }"></div>
        </div>
      </div>
      <div v-if="done_daily_quiz_flag" class="buttons-grid">
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
      <div v-else class="buttons-grid">
        <button @click="next_page('dailyquiz')">
          <img src="@/assets/titles/DailyQuiz.png" alt="Logo"/>
        </button>
        <button class="closed" @click="count_click()">
          <img src="@/assets/titles/CategoryQuiz.png" alt="Logo"/>
        </button>
        <button class="closed" @click="count_click()">
          <img src="@/assets/titles/RoadSign.png" alt="Logo"/>
        </button>
        <button class="closed" @click="count_click()">
          <img src="@/assets/titles/HazardPerception.png" alt="Logo"/>
        </button>
        <button class="closed" @click="count_click()">
          <img src="@/assets/titles/CrashQuizOff.png" alt="Logo"/>
        </button>
        <button class="closed" @click="count_click()">
          <img src="@/assets/titles/MockTest.png" alt="Logo"/>
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import toastr from 'toastr';
export default {
  name: "dashboard",
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      logged_in_user: this.$store.state.currentUser,
      achievements: this.$store.state.currentAchievements,
      done_daily_quiz_flag: this.$store.state.currentDoneDailyQuizFlag,
      clicks: 0
    };
  },
  methods: {
    info_message(title, msg) {
      toastr.info(msg, title, {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-top-right",
          timeOut: 1000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut",
          preventDuplicates: true
        });
    },
    warning_message(title, msg) {
      toastr.warning(msg, title, {
          closeButton: true,
          progressBar: true,
          positionClass: "toast-top-right",
          timeOut: 1000,
          showMethod: "fadeIn",
          hideMethod: "fadeOut",
          preventDuplicates: true
        });
    },
    count_click() {
      if (this.$store.state.currentAchievements.includes('You bloody rat')) {
        this.warning_message("Start with today's Daily Quiz!"," ");
      } else {
        // Increment click counter
        this.clicks += 1;
        if (this.clicks === 50) {
          this.add_achievement('You bloody rat','🐀');
        }
        if (this.clicks >= 40) {
          this.warning_message("...",' ');
        }
        if (this.clicks >= 30) {
          this.warning_message('Ok this is starting to annoy me.',' ');
        }
        if (this.clicks >= 20) {
          this.warning_message('Yo bro, just do the quiz.',' ');
        }
        if (this.clicks >= 10) {
          this.warning_message('Uhm, what are you doing?',' ');
        } else {
          this.warning_message("Start with today's Daily Quiz!"," ");
        }
      }
    },
    logout() {
      // Let server know the user is logging out.
      this.client_socket.emit('logout', this.logged_in_user);

      // Reset state of the store
      this.$store.commit("setCurrentUser", "");
      this.$store.commit("setCurrentPassword", "");
      this.$store.commit("setCurrentRank", { level: 'n/a', exp: 0, exp_threshold: 0 });
      this.$store.commit("setCurrentStats", { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a' });
      this.$store.commit("setCurrentAchievements", []);
      this.$store.commit("setCurrentRecentCatScores",{"Driving Off": [], "Urban Driving": [], "Rural Driving": [], "Bigger Roads": [], "Motorways": [], "Tricky Conditions": [], "Breakdowns": []});
      this.$store.commit("setCurrentSocialLists", { friends: [], friend_requests: [] });
      this.$store.commit("setCurrentLeaderboards", {public: [], friends: []});
      console.log("User logged out");

      this.next_page('authentication');
    },
    async load_friends_list() {
      this.info_message('Loading socials page ...', ' ');
      const response = await this.azure_function("POST", "/user/friend/all", { username: this.logged_in_user });
      if (response.result) {
        this.$store.commit("setCurrentSocialLists", {
          friends: response.msg.friends,
          friend_requests: response.msg.friend_requests
        });
        this.next_page('friends');
      }
    },
    async load_leaderboards() {
      this.info_message('Loading leaderboards ...', ' ');
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
            console.log(name + " achievement already unlocked.");
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
      // Send a request to the function app.
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
        console.log("Result:", JSON.stringify(result.result));
        return result;
      } catch (error) {
        console.error("Error:", error);
      }
    },
    next_page(page) {
      console.log("/" + page);
      this.$router.push(`/${page}`);
    },
  },
  computed: {
    progress_bar_width() {
      const sums = {};
      // Step 1: Sum for each category
      for (const category in this.$store.state.currentRecentCatScores) {
        const scores = this.$store.state.currentRecentCatScores[category];
        const sum = scores.reduce((acc, score) => acc + score, 0);
        sums[category] = sum;
      }
      // Step 2: Add all the sums
      const totalSum = Object.values(sums).reduce((acc, val) => acc + val, 0);
      
      // Step 3: Divide by 70 and convert to percentage
      const finalPercentage = ((totalSum / 70) * 100).toFixed(1);

      // Step 4: Return as a number (not string), or 0 if NaN
      return parseFloat(finalPercentage) || 0;
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

.buttons-grid button.closed {
  filter: grayscale(100%);
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
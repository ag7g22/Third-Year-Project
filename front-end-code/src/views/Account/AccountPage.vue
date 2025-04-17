<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div v-if="this.view === 'friends_list'" class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button @click="go_to_own_account()"> 👤 Account</button>
        <button disabled> 👥 Social Hub</button>
        <button @click="load_leaderboards"> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
      </div>
    </div>
    <div v-else-if="this.view === 'leaderboard'" class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button @click="go_to_own_account()"> 👤 Account</button>
        <button @click="load_friends_list"> 👥 Social Hub</button>
        <button disabled> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
      </div>
    </div>
    <div v-else class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button disabled> 👤 Account</button>
        <button @click="load_friends_list"> 👥 Social Hub</button>
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

        <!-- Middle: User Stats -->
        <div class="user-stats">
          <p>ID: {{ stats.id }}</p>
          <p>Daily Score: {{ stats.daily_training_score }}</p>
          <p>Daily Completed: {{ stats.training_completion_date }}</p>
        </div>

        <div v-if="current_view === 'achievements'">
          <h3>Achievements</h3>
          <div class="achievements-box" v-if="user_achievements.length">
            <ul>
              <li v-for="achievement in user_achievements" :key="achievement.name" :class="{ locked: !achievement.unlocked }">
                <div class="achievement-content">
                  <div class="achievement-emoji">{{ achievement.emoji }}</div>
                  <div>
                    <div class="achievement-name">{{ achievement.name }}</div>
                    <div class="achievement-description">{{ achievement.description }}</div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Bottom: Graph Box -->
        <div v-if="current_view === 'overall'">
          <h3>Overall Stats</h3>
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

      </div>

      <!-- Buttons -->
      <div v-if="view !== 'logged_user'">
        <div class="game-buttons">
          <button class="game-button" @click="handleBack">Return</button>
          <button
            v-for="view in ['achievements', 'overall']"
            :key="view"
            @click="toggle_view(view)"
            :disabled="current_view === view"
            class="game-button"
          >
            {{ formatViewName(view) }}
          </button>
        </div>
      </div>
      <div v-else>
        <div class="game-buttons">
          <button
            v-for="view in ['achievements', 'overall']"
            :key="view"
            @click="toggle_view(view)"
            :disabled="current_view === view"
            class="game-button"
          >
            {{ formatViewName(view) }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import toastr from 'toastr';
export default {
  name: "account",
  mounted() {
      if (this.view !== 'logged_user' && this.username !== this.logged_in_user) {
        this.add_achievement('STALKER!','👀');
      }
  },
  data() {
    return {
      current_view: 'achievements', // View only accounts only show the achievements
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
        { name: 'Start of a Journey', description: 'Logged into GearUp! for the first time as a new learner!', emoji: '🔑' }, //
        // Exploring all the main quiz games:
        { name: 'Day One Done', description: 'Done a DAILY QUIZ for the first time.', emoji: '💡' }, //
        { name: 'Switchin Gears', description: 'Done a CATEGORY QUIZ for the first time.', emoji: '🔎' }, //
        { name: 'A Sign of Things to Come', description: 'Done a ROAD SIGN quiz for the first time.', emoji: '🛑' },//
        { name: 'Eyes on the Road', description: 'Done HAZARD PERCEPTION for the first time.', emoji: '💀' },//
        { name: '1 v 1 me rn m8', description: 'Done CRASH QUIZ OFF for the first time.', emoji: '💥' },//
        { name: 'Mock & Roll', description: 'Done a MOCK TEST for the first time.', emoji: '📖' },//
        // Daily Quiz Challenges:
        { name: 'ITS OVER 9000!', description: 'Get a daily score of over 9000 in the first attempt of the day', emoji: '🤯' }, //
        { name: 'The Dragon Warrior', description: 'Come first in the TOP 10 in the PUBLIC daily leaderboard!', emoji: '🐉' }, //
        { name: 'In your face!', description: 'Come first in the TOP 10 in the FRIEND daily leaderboard!', emoji: '🤪' }, //
        // Category Quiz challenges:
        { name: 'Transform and roll out!', description: 'Get 100% score for 20 questions in the "Driving Off" category quiz.', emoji: '🚗' },//
        { name: "I'm from the city", description: 'Get 100% score for 20 questions in the "Urban Driving" category quiz.', emoji: '🏙️' },//
        { name: 'A force of nature', description: 'Get 100% score for 20 questions in the "Rural Driving" category quiz.', emoji: '🌳' },//
        { name: "Size doesn't matter", description: 'Get 100% score for 20 questions in the "Bigger Roads" category quiz.', emoji: '🛤️' },//
        { name: 'King of the Motorways', description: 'Get 100% score for 20 questions in the "Motorways" category quiz.', emoji: '🛣️' },//
        { name: 'The weather forcaster', description: 'Get 100% score for 20 questions in the "Tricky Conditions" category quiz.', emoji: '🌧️' },//
        { name: 'Oopsies!', description: 'Get 100% score for 20 questions in the "Breakdowns" category quiz.', emoji: '⚠️' },//
        // Road Sign Challenges:
        { name: 'Mastering the Sign language', description: 'Get 100% score for 12 questions in a ROAD SIGN QUIZ.', emoji: '🚦' }, //
        // Hazard Perception Challenges:
        { name: 'Where are you clicking lil bro', description: 'Click more than 10 times in the hazard perception practice.', emoji: '🚩' },//
        { name: 'Takin out the trash', description: 'Get 5/5 score in a certain hazard perception video.', emoji: '🗑️' },//
        { name: 'NEIGHHHHHH!', description: 'Get 5/5 score in a certain hazard perception video.', emoji: '🐎' },//
        { name: 'Fireman sam', description: 'Get 5/5 score in a certain hazard perception video.', emoji: '👨‍🚒' },//
        { name: 'Oh deer', description: 'Get 5/5 score in a certain hazard perception video.', emoji: '🦌' },//
        { name: 'You snooze you lose!', description: 'Get 5/5 score in a certain hazard perception video.', emoji: '💤' },//
        // Crash Quiz Off Challenges:
        { name: 'The Crash-off King', description: 'Win a CRASH QUIZ OFF GAME (without any players quitting).', emoji: '👑' },//
        { name: 'Yes king', description: 'Lose a CRASH QUIZ OFF GAME (without any players quitting).', emoji: '🥀' },//
        { name: 'The Crash-out King', description: 'Quit a CRASH QUIZ OFF GAME.', emoji: '🏳️' },//
        // Mock Exam Challenges:
        { name: '"Just put the license in the bag bro"', description: 'Score 100% on a mock exam.', emoji: '💯' },//
        // Friend Achievements:
        { name: 'STALKER!', description: 'View another user profile', emoji: '👀' }, //
        { name: 'Request for alliance', description: 'Send a friend request.', emoji: '📨' },//
        { name: 'A remarkable ally', description: 'Accept a friend request.', emoji: '🤝' },//
        { name: 'A sworn enemy', description: 'Remove a friend.', emoji: '💔' },//
        // Stat Achievements:
        { name: 'Absolute Bang out', description: 'Reached level 20.', emoji: '🤓' }, 
        { name: 'You bloody rat', description: "If you get this achievement you're a rat.", emoji: '🐀' }, 
        { name: 'Thank you for playing my game!', description: 'Reached a streak of 7!', emoji: '🔥' }, //
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
    };
  },
  computed: {
    user_achievements() {
      return this.achievementsWithDescriptions.map(a => {
        const unlocked = this.achievements.includes(a.name);
        return {
          ...a,
          unlocked,
          emoji: unlocked ? a.emoji : '🔒'
        };
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
    },
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
    toggle_view(view) {
      this.current_view = view;
    },
    formatViewName(view) {
      const mapping = {
        overall: "Overall Stats",
        category: "Category Stats",
        forget: "Forgetting Curve"
      };
      return mapping[view] || view;
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
            timeOut: 7000,
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
    go_to_own_account() {
      // Go to own account from friend account
      this.current_view = 'achievements';
      this.view = 'logged_user';
      this.username = this.$store.state.currentUser;
      this.rank = this.$store.state.currentRank;
      this.stats = this.$store.state.currentStats;
      this.achievements = this.$store.state.currentAchievements;
      this.recent_category_scores = this.$store.state.currentRecentCatScores;
      this.current_list = "friends";
      this.search = { query: "", users: [] };
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
  margin-bottom: 10px;
}

.exp-bar-fill {
  height: 100%;
  background-color: #079cb0;
  transition: width 0.3s ease-in-out;
}

.user-stats {
  color: #f3af59;
  display: flex;
  text-align: left;
  justify-content: center;
  gap: 20px;
  margin-bottom: 15px;
}

.graph-box,
.achievements-box {
    color: #ffffff;
    background-color: black;
    border: 2px solid #f3af59;
    width: 100%;
    max-width: 1400px;
    height: 40vh;
    padding: 20px;  /* More internal padding */
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
}

.achievements-box ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.achievements-box li {
  text-align: left;
  background-color: #1a1a1a;
  border: 1px solid #f3af59;
  padding: 12px 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
}

.achievement-content {
  display: flex;
  gap: 16px;
  align-items: center;
}

.achievement-emoji {
  font-size: 2rem;
  width: 2.5rem;
}

.achievement-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 4px;
}

.achievement-description {
  font-size: 0.9rem;
  color: #cccccc;
}

/* Locked styling */
.locked {
  opacity: 0.4;
}

</style>
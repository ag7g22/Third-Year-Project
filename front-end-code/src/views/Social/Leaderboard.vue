<template>
  <div class="sidebar-main-layout">
    <!-- Sidebar -->
    <div class="sidebar">
      <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
      <div class="side-buttons">
        <button @click="next_page('dashboard')"> 🎲 Dashboard</button>
        <button @click="next_page('account')"> 👤 Account</button>
        <button @click="load_friends_list"> 👥 Social Hub</button>
        <button disabled> 🏆 Leaderboard</button>
        <button @click="logout"> 🔒 Log out</button> 
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
          <h3 v-else>Damn, no one has done the daily quiz yet. Bunch of procrasinators!</h3>
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
          <h3 v-else>Where yo friends at? They're lacking right now</h3>
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
import toastr from 'toastr';
export default {
  name: "leaderboard",
  mounted() {
    if (this.leaderboards.public.length >= 10 && this.leaderboards.public[0] === this.logged_in_user) {
      this.add_achievement('The Dragon Warrior','🐉');
    }
    if (this.leaderboards.friends.length >= 10 && this.leaderboards.friends[0] === this.logged_in_user) {
      this.add_achievement('In your face!','🤪');
    }
  },
  data() {
    return {
      client_socket: this.$store.state.currentClientSocket,
      current_list: "public",
      logged_in_user: this.$store.state.currentUser,
      leaderboards: this.$store.state.currentLeaderboards,
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
          preventDuplicates: false
      });
    },
    error_message(title, msg) {
    toastr.error(msg, title, {
        closeButton: true,
        progressBar: true,
        positionClass: "toast-top-right",
        timeOut: 1000,
        showMethod: "fadeIn",
        hideMethod: "fadeOut",
        preventDuplicates: true
        });
    },
    toggle_list(list) {
      this.current_list = list;
    },
    async view_user(username) {
      this.info_message('Loading user profile ...', ' ');
      if (username === this.logged_in_user) {
        next_page('account');
        return;
      }
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
<template>
  <div class="container">
    <h1 class="title">DASHBOARD | {{ logged_in_user }}</h1>
    <div class="buttons">
      <button @click="next_page('account')">Account</button>
      <button @click="load_friends_list">Friends</button>
      <button @click="next_page('dailyquiz')">Daily Training</button>
      <button @click="next_page('lobby')">Versus</button>
      <button @click="next_page('categoryquiz')">Category Practice</button>
      <button @click="next_page('roadsignquiz')">Road Sign Practice</button>
      <button @click="next_page('hazard')">Hazard Perception</button>
      <button @click="next_page('mockexam')">Mock Exam</button>
      <button @click="load_leaderboards">Leaderboard</button>
      <button @click="logout">Log out</button>
    </div>
    <p v-if="message.error" class="error-message">{{ message.error }}</p>
    <p v-if="message.success" class="success-message">{{ message.success }}</p>
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
  }
};
</script>

<style lang="scss" scoped>



</style>
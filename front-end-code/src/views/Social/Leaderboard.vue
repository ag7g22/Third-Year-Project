<template>
    <div class="container">
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
  </template>
  
  <script>
  export default {
    name: "leaderboard",
    data() {
      return {
        current_list: "public",
        logged_in_user: this.$store.state.currentUser,
        leaderboards: this.$store.state.currentLeaderboards,
        message: { error: "", success: "" },
      };
    },
    methods: {
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
      async azure_function(method, route, data) {
        try {
          const url = `${process.env.VUE_APP_BACKEND_URL}${route}?code=${process.env.VUE_APP_MASTER_KEY}`;
          const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });
          return await response.json();
        } catch (error) {
          console.error("Azure Function Error:", error);
          this.message.error = "An API error occurred. Please try again later.";
        }
      },
      next_page(page) {
        this.$router.push(`/${page}`);
      },
    },
  };
  </script>
  
  <style lang="scss" scoped>
  </style>
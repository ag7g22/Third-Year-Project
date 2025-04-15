<template>
    <!-- This is the navigation menu for the different pages (Testing purposes only) -->
    <header>
        <div v-if="this.$route.name === 'mainPage'" class="header-title">
          <h1>Welcome!</h1>
        </div>
        <div v-if="this.$route.name === 'authentication'" class="header-title">
          <h1>Sign in to GearUp!</h1>
        </div>
        <div v-if="this.$route.name === 'dashboard'" class="header-title">
          <h1>Welcome {{ this.$store.state.currentUser }}! What are we practicing today?</h1>
        </div>
        <div v-if="this.$route.name === 'account'" class="header-title">
          <h1>User profile</h1>
        </div>
        <div v-if="this.$route.name === 'friends'" class="header-title">
          <h1>Social Hub</h1>
        </div>
        <div v-if="this.$route.name === 'leaderboard'" class="header-title">
          <h1>Daily Quiz Leaderboards</h1>
        </div>
        <div v-if="this.$route.name === 'lobby'" class="header-title">
          <h1>1 vs 1 Quiz battle</h1>
        </div>
        <div v-if="this.$route.name === 'categoryquiz'" class="header-title">
          <h1>Category Quiz</h1>
        </div>
        <div v-if="this.$route.name === 'roadsignquiz'" class="header-title">
          <h1>Road Sign Quiz</h1>
        </div>
        <div v-if="this.$route.name === 'feedback'" class="header-title">
          <h1>Question feedback</h1>
        </div>
        <div v-if="this.$route.name === 'dailyquiz'" class="header-title">
          <h1>Daily training session</h1>
        </div>
        <div v-if="this.$route.name === 'mockexam'" class="header-title">
          <h1>Mock Test</h1>
        </div>
        <div v-if="this.$route.name === 'hazard'" class="header-title">
          <h1>Hazard Perception</h1>
        </div>
        <div v-if="this.$route.name === 'HPvideo'" class="header-title">
          <h1>Video clip practice</h1>
        </div>
    </header>
</template>

<script>
// Vue Component, to be referenced in other parts of the app:
import io from 'socket.io-client';

export default {
    name: 'Header',
    mounted: function() {
        this.connect(); 
    },
    data() {
      return {
        appName: "GearUp"
      };
    },
    methods: {
        // Connect the client to the server
        connect() {
            var socket = io();
            this.$store.commit("setCurrentClientSocket", socket);
            console.log("Client-Socket JOINED: ", this.$store.state.currentClientSocket);
        },
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
}

</script>

<style lang="scss" scoped>
header {
  background-color: rgb(20, 20, 20);
  text-align: center;
  height: 80px; /* Set a fixed height for the header */
  width: 100%; /* Ensure it stretches across the entire width of the screen */
  box-sizing: border-box; /* Include padding and border in the height calculation */
  display: flex;
  align-items: center; /* Vertically center the content inside the header */
  justify-content: center; /* Horizontally center the navigation items */
}

h1 {
  color: #ffffff; /* White text */
  text-decoration: none;
  font-weight: bold;
  padding: 10px 15px; /* Some padding for the links */
  display: inline-block; /* Make the links clickable and properly sized */
}
</style>
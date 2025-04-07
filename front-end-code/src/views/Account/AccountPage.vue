<template>
    <div class="container">
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
  
      <!-- Navigation Buttons -->
      <div class="buttons">
        <button @click="handleBack">Back</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "account",
    data() {
      return {
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
      next_page(page) {
        this.$router.push({ path: `/${page}` });
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
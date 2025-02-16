<template>
    <div class="container">
        <h1 class="title">ACCOUNT | {{ username }}</h1>

        <!-- User Stats -->
        <div>
            <div>
                <p>ID: {{ stats.id }} </p>
                <p>LEVEL {{ rank.level }}</p>
                <p>EXP: {{ rank.exp }} / {{ rank.exp_threshold }}</p>
                <p>STREAK: {{ stats.streak }} </p>
                <p>Daily Score: {{ stats.daily_training_score }} </p>
                <p>Daily Quiz Completed: {{ stats.training_completion_date }} </p>   
            </div>
        </div>

        <!-- Achievements Box -->
        <div v-if="achievements && achievements.length" class="achievements-box">
            <h3>Achievements</h3>
            <ul>
                <li v-for="achievement in user_achievements">
                    {{ achievement.name }} - {{ achievement.description }}
                </li>
            </ul>
        </div>

        <!-- If the view is for the logged in user -->
        <div v-if="view === 'logged_user'" class="buttons">
            <button @click="next_page('dashboard')">Back</button>
            <button @click="next_page('update')">Update details</button> 
        </div>

        <!-- If the view is for viewing another user from friends_list page -->
        <div v-else-if="view === 'friends_list'" class="buttons"> 
            <button @click="next_page('friends')">Back</button>
        </div>

        <!-- If the view is for viewing another user from leaderboard page -->
        <div v-else-if="view === 'leaderboard'" class="buttons"> 
            <button @click="next_page('leaderboard')">Back</button>
        </div>
        
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "account",
    mounted() {
        // When you view the random user
        this.view = this.$route.query.view || 'logged_user';
        this.username = this.$route.query.username || this.$store.state.currentUser;
        this.rank = this.$route.query.rank || this.$store.state.currentRank;
        this.stats = this.$route.query.stats || this.$store.state.currentStats;
        this.achievements = this.$route.query.achievements || this.$store.state.currentAchievements;

        // Saving state of friendsList:
        this.current_list = this.$route.query.current_list || "friends";
        this.search = this.$route.query.search || { query: "", users: [] };
    },
    data() {
        return {
            // Default view is the logged in user
            view: 'logged_user',
            username: this.$store.state.currentUser,
            rank: this.$store.state.currentRank,
            stats: this.$store.state.currentStats,
            achievements: this.$store.state.currentAchievements,

            // All of the achievements:
            achievementsWithDescriptions: [
                { name: 'Hello World!', description: 'Unlocked after logging in for the first time.' },
                { name: 'Start of a Journey', description: 'Done a daily quiz for the first time.' },
                { name: 'Levelin up', description: 'Reached level 10 for the first time.' },
                { name: 'Gear 2nd', description: 'Reached a streak of 10' },
                { name: 'Gear 3rd', description: 'Reached a streak of 50' },
                { name: 'Gear 4th', description: 'Reached a streak of 100' },
                { name: 'Gear 5th', description: 'Reached a streak of 500' },
            ],

            // State of friendsList page saved here.
            current_list: "friends", 
            search: { query: "", users: [] } 
        };
    },
    methods: {
        formatLabel(key) {
            return key.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
        },
        formatValue(value) {
            return value === "n/a" ? "Not Available" : value;
        },
        next_page(page) {
            console.log("/" + page);
    
            if (page === 'friends') {
                this.$router.push({
                    path: `/friends`,
                    query: { current_list: this.current_list, search: this.search }
                });
                return;
            }

            this.$router.push(`/${page}`);
        }
    },
    computed: {
        user_achievements() {
        // Return a new list by filtering the achievementsWithDescriptions
        return this.achievements.map((name) => {
            const achievement = this.achievementsWithDescriptions.find(
            (item) => item.name === name
            );
            return achievement ? achievement : { name: name, description: 'No description available' };
        });
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
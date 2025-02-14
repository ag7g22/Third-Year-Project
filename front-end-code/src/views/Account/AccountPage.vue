<template>
    <div class="container">
        <h1 class="title">ACCOUNT | {{ username }}</h1>
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
        <!-- If the view is for the logged in user -->
        <div v-if="view === 'logged_user'" class="buttons">
            <button @click="next_page('dashboard')">Back</button>
            <button @click="next_page('update')">Update details</button> 
        </div>

        <!-- If the view is for viewing another user -->
        <div v-else class="buttons"> 
            <button @click="next_page('friends')">Back</button>
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
    },
    data() {
        return {
            // Default view is the logged in user
            view: 'logged_user',
            username: this.$store.state.currentUser,
            rank: this.$store.state.currentRank,
            stats: this.$store.state.currentStats
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
            console.log("Moving on to the " + page + " page!");
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
</style>
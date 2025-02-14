<template>
    <div class="container">
        <h1 class="title">LEADERBOARD | {{ logged_in_user }}</h1>
        <div class="buttons">
            <button @click="next_page('dashboard')">Back</button>
        </div>
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "leaderboard",
    data() {
        return {
            logged_in_user: this.$store.state.currentUser,
        };
    },
    methods: {
        next_page(page) {
            console.log("/" + page);
            this.$router.push(`/${page}`);
        }
    },
};
</script>

<style lang="scss" scoped>
</style>
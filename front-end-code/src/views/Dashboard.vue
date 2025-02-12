<template>
    <div class="container">
        <h1 class="title">DASHBOARD | {{ logged_in_user }}</h1>
        <div class="buttons">
            <button @click="next_page('account')">Account</button>
            <button>Friends</button>
            <button>Daily Training</button>
            <button>Category Practice</button>
            <button>Road Sign Practice</button>
            <button @click="logout()">Log out</button>   
        </div>
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "dashboard",
    data() {
        return {
            logged_in_user: this.$store.state.currentUser
        };
    },
    methods: {
        logout() {
            this.$store.commit("setCurrentUser", "");
            this.$store.commit("setCurrentPassword", "");
            this.$store.commit("setCurrentStats", { id: 'n/a', streak: 0, daily_training_score: 0, training_completion_date: 'n/a'});
            console.log("Current User and Password:", this.$store.state.currentUser, this.$store.state.currentPassword);
            this.next_page('authentication')
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
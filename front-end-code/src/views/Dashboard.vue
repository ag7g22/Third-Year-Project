<template>
    <div class="container">
        <h1 class="title">DASHBOARD</h1>
        <div class="buttons">
            <button>Account</button>
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
            
        };
    },
    methods: {
        logout() {
            this.$store.commit("setCurrentUser", "");
            this.$store.commit("setCurrentPassword", "");
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
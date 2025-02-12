<template>
    <div class="container">
        <h1 class="title">ACCOUNT | {{ logged_in_user }}</h1>
        <div>
        <ul>
            <li v-for="(value, key) in stats" :key="key">
                <strong>{{ formatLabel(key) }}:</strong> {{ formatValue(value) }}
            </li>
        </ul>  
        </div>
        <div class="buttons">
            <button @click="next_page('dashboard')">Back</button>
           <button @click="next_page('update')">Update details</button> 
        </div>
        
    </div>
</template>
  
<script>
export default {
    // Page member variables and methods:
    name: "account",
    data() {
        return {
            logged_in_user: this.$store.state.currentUser,
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
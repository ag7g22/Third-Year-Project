<template>
  <div class="container">
    <h1 class="title">Welcome to <span>{{ appName }}</span>!</h1>
    <div class="buttons">
      <button @click="next_page('authentication')">Sign in</button>
    </div>
  </div>
</template>

<script>
  export default {
    // Page member variables and methods:
    name: "mainPage",
    data() {
      return {
        appName: "Vroom Vroom Quiz"
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
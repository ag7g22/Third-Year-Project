<template>
  <!-- This is the root component of a Vue.js application. -->
  <div id="app">
    <!-- Custom component imported from ./components/Header.vue -->
    <Header />
    <!-- Vue Router placeholder that dynamically loads components based on the current route. -->
    <router-view></router-view>
  </div>
</template>

<script>
  import Header from './components/Header'
  export default {
    name: 'App',
    components: {
      Header
    }
  }
</script>

<style>
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
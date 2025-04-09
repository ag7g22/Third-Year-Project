<template>
    <!-- This is the navigation menu for the different pages (Testing purposes only) -->
    <header>
        <nav>
            <ul>
                <li><router-link to="/authentication">Authentication</router-link></li>
            </ul>
        </nav>
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
  background-color: #10012a; /* Dark purple */
  text-align: center;
  height: 80px; /* Set a fixed height for the header */
  width: 100%; /* Ensure it stretches across the entire width of the screen */
  box-sizing: border-box; /* Include padding and border in the height calculation */
  display: flex;
  align-items: center; /* Vertically center the content inside the header */
  justify-content: center; /* Horizontally center the navigation items */
}

nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center; /* Center the navigation links */
}

nav ul li {
  display: inline;
  margin-right: 10px; /* Space between items */
}

nav ul li a {
  color: #ffffff; /* White text */
  text-decoration: none;
  font-weight: bold;
  padding: 10px 15px; /* Some padding for the links */
  display: inline-block; /* Make the links clickable and properly sized */
}

nav ul li a:hover {
  text-decoration: underline;
}
</style>
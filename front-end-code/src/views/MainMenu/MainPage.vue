<template>
  <div class="main-container">
      <div class="content">
        <img src="@/assets/titles/TitleLogo.png" alt="Logo" class="logo" />
        <p class="title-text">The Ultimate Driving Theory Game</p>
      </div>
      <button @click="next_page('authentication')" class="menu-button">Start game</button>
      <p class="footer-text">@ag7g22 3rd Yr Project</p>
  </div>
</template>

<script>
  export default {
    name: "mainPage",
    methods: {
      next_page(page) {
        console.log("/" + page);
        this.$router.push(`/${page}`);
      }
    },
  };
</script>

<style lang="scss" scoped>
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: calc(100vh - 80px); /* 100% of the screen height minus the header's height */
    background-color: rgb(28, 27, 27);
    overflow: hidden; /* Prevent content from overflowing */
}

.content {
  top: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-grow: 1; /* Ensure it takes available space */
}

.logo {
  width: 500px;
  margin-bottom: 20px;

  /* Add animation */
  animation: floatSpinScale 6s ease-in-out infinite;
}

/* Keyframes for rotating and scaling */
@keyframes floatSpinScale {
  0% {
    transform: rotate(0deg) scale(1);
  }
  20% {
    transform: rotate(0.5deg) scale(1.02);
  }
  40% {
    transform: rotate(1deg) scale(1.03);
  }
  60% {
    transform: rotate(0.5deg) scale(1.02);
  }
  80% {
    transform: rotate(-0.5deg) scale(1.01);
  }
  100% {
    transform: rotate(0deg) scale(1);
  }
}

.title-text {
  color: #fff; /* Change text color to white on hover */
  font-size: 20px; /* Increase the font size */
}

.menu-button {
  color: #f3af59; /* Set the text color to the original color */
  font-size: 25px; /* Increase the font size */
  padding: 15px 30px; /* Increase padding for a larger button */
  position: absolute;
  bottom: 20px; /* Position at the bottom left */
  left: 20px;
  border: none; /* Remove the border */
  background: none; /* Remove the background */
  cursor: pointer;
}

.menu-button:hover {
  color: #fff; /* Change text color to white on hover */
  transform: scale(1.05); /* Slight zoom without layout shift */
}

.footer-text {
  color: #fff; /* Change text color to white on hover */
  font-size: 25px; /* Increase the font size */
  padding: 15px 30px; /* Increase padding for a larger button */
  position: absolute;
  bottom: 20px; /* Position at the bottom right */
  right: 20px;
}
</style>
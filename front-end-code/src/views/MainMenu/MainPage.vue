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
  height: calc(100vh - 80px);
  background-color: rgb(30, 30, 30);
  overflow: hidden;
}

.content {
  top: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
}

.logo {
  width: 500px;
  margin-bottom: 20px;
  animation: floatSpinScale 6s ease-in-out infinite;
}

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
  color: #fff;
  font-size: 20px;
}

.menu-button {
  color: #f3af59;
  font-size: 25px;
  padding: 15px 30px;
  position: absolute;
  bottom: 20px;
  left: 20px;
  border: none;
  background: none;
  cursor: pointer;
}

.menu-button:hover {
  color: #fff;
  transform: scale(1.05);
}

.footer-text {
  color: #fff;
  font-size: 25px;
  padding: 15px 30px;
  position: absolute;
  bottom: 20px;
  right: 20px;
}
</style>
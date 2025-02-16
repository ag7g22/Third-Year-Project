import Vue from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';
import './assets/main.css';
import 'toastr/build/toastr.min.css';

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
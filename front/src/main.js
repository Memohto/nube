import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { initializeApp } from "firebase/app";

import '@fortawesome/fontawesome-free/js/all.js';

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

const firebaseConfig = {
  apiKey: "AIzaSyB33WNvEv9-SBciuOZK2A8ZUbRO14fwc5k",
  authDomain: "nubes-e8905.firebaseapp.com",
  databaseURL: "https://nubes-e8905-default-rtdb.firebaseio.com",
  projectId: "nubes-e8905",
  storageBucket: "nubes-e8905.appspot.com",
  messagingSenderId: "817092808004",
  appId: "1:817092808004:web:1eadae3aaa6239ecb25b11",
  measurementId: "G-R26W0EHCVW"
};

initializeApp(firebaseConfig);

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

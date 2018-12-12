import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'

import Vuikit from 'vuikit'
import VuikitIcons from '@vuikit/icons'
import '@vuikit/theme'

import axios from 'axios'
import VueAxios from 'vue-axios'

import Toasted from 'vue-toasted';

Vue.use(Vuikit)
Vue.use(VuikitIcons)
Vue.use(VueAxios, axios)
Vue.use(Toasted)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

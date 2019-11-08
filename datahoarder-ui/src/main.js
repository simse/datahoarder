import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'

import axios from 'axios'
import VueAxios from 'vue-axios'

import Toasted from 'vue-toasted'
import VueMatchHeights from 'vue-match-heights'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faTrashAlt, faSync, faArrowLeft } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTrashAlt)
library.add(faSync)
library.add(faArrowLeft)
 
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(VueAxios, axios)
Vue.use(Toasted)
Vue.use(BootstrapVue)
Vue.use(VueMatchHeights)

Vue.config.productionTip = false

Vue.mixin({
    data: function() {
        return {
            get datahoarder_url() {
                return '//' + window.location.hostname + ':4040/api/'
            },
            no_connection: false
        }
    }
})

document.title = 'Datahoarder'

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

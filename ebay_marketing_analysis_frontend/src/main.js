import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
// Library Components
import VueSweetalert2 from 'vue-sweetalert2'
import VueApexCharts from 'vue3-apexcharts'
import BootstrapVue3 from 'bootstrap-vue-3'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import CounterUp from 'vue3-autocounter'
import '@mdi/font/css/materialdesignicons.css';
import 'aos/dist/aos.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

// Custom Components & Directives
import globalComponent from './plugins/global-components'
import globalDirective from './plugins/global-directive'
import globalMixin from './plugins/global-mixin'
import Vue3Toasity from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

require('waypoints/lib/noframework.waypoints.min')

const app = createApp(App)
const vuetify = createVuetify({
  components,
  directives,
  })

app.use(store).use(router)
// Library Components
app.use(ElementPlus)
app.use(Vue3Toasity);
app.use(VueSweetalert2)
app.use(VueApexCharts)
app.use(BootstrapVue3)
app.component('counter-up', CounterUp)

// Custom Components & Directives
app.use(globalComponent)
app.use(globalDirective)
app.use(vuetify)
app.mixin(globalMixin)

app.mount('#app')

export default app

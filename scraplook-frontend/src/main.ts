import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import router from './router/router'



import 'primevue/resources/themes/aura-light-green/theme.css'

const app = createApp(App)


app.use(PrimeVue)
app.use(router)

app.mount('#app')

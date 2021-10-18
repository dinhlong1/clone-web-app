import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import SideBar from './components/client/SideBar.vue'
import Navbar from './components/client/Navbar.vue'
import Footer from './components/client/Footer.vue'
import SideBarAdmin from './components/admin/SideBarAdmin.vue'
import NavbarAdmin from './components/admin/NavbarAdmin.vue'
import FooterAdmin from './components/admin/FooterAdmin.vue'



axios.defaults.baseURL = 'http://127.0.0.1:8000/' 
createApp(App)
.use(router)
.use(store)
.use(router,axios)
.component('SideBar',SideBar).component('Navbar',Navbar)
.component('SideBarAdmin',SideBarAdmin)
.component('NavbarAdmin',NavbarAdmin)
.component('FooterAdmin',FooterAdmin)
.component('Footer',Footer)
.mount('#app')

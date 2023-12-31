import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import DropZone from 'dropzone-vue';

// optionally import default styles
import 'dropzone-vue/dist/dropzone-vue.common.css';
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


createApp(App).use(store).use(router).use(DropZone).mount('#app')

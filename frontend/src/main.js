import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Chatbot from './components/Chatbot.vue';
import Header from '@/components/Header.vue';
createApp(App)
.component('Chatbot', Chatbot)
.component('Header', Header)
.use(router)
.mount('#app');

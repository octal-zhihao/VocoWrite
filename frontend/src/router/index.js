import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Record from '../views/Record.vue'; // 录音界面

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/record',
    name: 'Record',
    component: Record,
  },
  // 其他页面...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

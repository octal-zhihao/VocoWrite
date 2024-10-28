import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Record from '../views/Record.vue'; // 录音界面
import FileImport from '../views/FileImport.vue'; // 导入文件界面

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
  {
    path: '/file-import', 
    name: 'FileImport',
    component: FileImport,
  },
  // 其他页面...
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

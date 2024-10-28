<template>
  <div class="app-container">
    <!-- 侧边栏折叠按钮 -->
    <button class="toggle-sidebar-btn" @click="toggleSidebar">☰</button>
    <!-- 引入侧边栏组件 -->
    <Sidebar :class="{ active: isSidebarVisible }" />

    <!-- 主内容区域 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <Header />

      <!-- 主内容区域渲染页面组件 -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import Header from './components/Header.vue';

export default {
  components: {
    Sidebar,
    Header,
  },
  data() {
      return {
        isSidebarVisible: false // 默认隐藏侧边栏
      };
    },
    methods: {
      toggleSidebar() {
        this.isSidebarVisible = !this.isSidebarVisible; // 切换侧边栏状态
      }
    }
  };
</script>

<style>
.app-container {
  display: flex;
  height: 100vh;
  background-color: #f4f6f8;
}

.main-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  margin-left: 15px;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2); 
  border-radius: 10px;
  overflow: hidden;
  height: calc(100vh - 20px); /* 适当调整高度 */
}

.content {
  margin-top: 10px;
  padding: 0px 30px; /* 适当增加内边距 */
  flex-grow: 1;
  overflow-y: auto; /* 允许纵向滚动 */
}


.toggle-sidebar-btn {
  display: none; /* 默认隐藏 */
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 2000;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
}

/* 媒体查询，适应小屏幕设备 */
@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .main-container {
    margin-left: 0;
  }
  
  .content {
    padding: 10px; /* 减小内边距 */
  }

  .toggle-sidebar-btn {
    display: block; /* 小屏幕显示按钮 */
  }
}
</style>

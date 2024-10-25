<template>
  <div class="app-container">
    <!-- 引入侧边栏组件 -->
    <Sidebar />

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
}


.content {
  margin-top: 10px;
  padding: 0px 30px; /* 适当增加内边距 */
  flex-grow: 1;
}

</style>
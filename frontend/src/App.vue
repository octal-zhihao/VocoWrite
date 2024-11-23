<template>
  <div class="app-container">
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
import Header from './components/Header.vue';

export default {
  components: {
    Header,
  },
};
</script>

<style>
body {
  margin: 0; /* 移除默认的外边距 */
}

.app-container {
  display: flex;
  height: 100vh; /* 确保app容器高度填满整个视口 */
  background-color: #f4f6f8;
}

.main-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2); 
  border-radius: 10px;
  overflow: hidden;
  height: 100vh; 
}

.content {
  padding: 0px 20px;
  flex-grow: 1;
}

</style>

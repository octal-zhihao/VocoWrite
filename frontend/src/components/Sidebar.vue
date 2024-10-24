<template>
  <div class="sidebar">
    <!-- Logo -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Logo" class="logo" />
      <span class="app-title">VocoWrite</span>
    </div>
    <ul class="menu">
      <li><i class="fas fa-file-alt"></i> 转写文件</li>
      <li @click="toggleSubmenu">
        <i class="fas fa-microphone"></i> 会记文件
        <i class="fas" :class="submenuOpen ? 'fa-chevron-up' : 'fa-chevron-down'" style="margin-left:auto;"></i>
      </li>
      <ul v-show="submenuOpen" class="submenu">
        <li><i class="fas fa-clock"></i> 最近文件</li>
        <li><i class="fas fa-folder"></i> 我的文件</li>
        <li><i class="fas fa-star"></i> 收藏文件</li>
        <li><i class="fas fa-trash"></i> 回收站</li>
      </ul>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      submenuOpen: false,
    };
  },
  methods: {
    toggleSubmenu() {
      this.submenuOpen = !this.submenuOpen;
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #eef1f6;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 0 8px 8px 0; /* 只在右侧添加圆角 */
}

.logo-container {
  display: flex;
  align-items: center;
  margin-bottom: 30px; /* 增加底部间距 */
}

.logo {
  height: 40px;
  margin-right: 10px;
}

.menu {
  list-style-type: none;
  padding: 0;
}

.menu li {
  position: relative;
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.menu li i {
  margin-right: 10px;
}

.menu li:hover {
  background-color: #d4d9e1;
  border-radius: 8px; /* 增加圆角效果 */
}

.submenu {
  list-style-type: none;
  padding-left: 20px; /* 加大子菜单的缩进 */
}

.submenu li i {
  margin-right: 10px;
}

.submenu li {
  padding: 10px 15px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease;
}

.submenu li:hover {
  background-color: #c4c9d1; /* 子菜单的悬停效果稍微更深 */
  border-radius: 5px;
}

</style>
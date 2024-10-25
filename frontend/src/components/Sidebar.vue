<template>
  <div class="sidebar">
    <!-- Logo -->
    <div class="logo-container">
      <img src="@/assets/logo3.png" alt="Logo" class="logo" />
      <span class="app-title">VocoWrite</span>
    </div>
    <ul class="menu">
      <!-- 转写文件 -->
      <li :class="{ active: selectedMenu === 'transcription' }" @click="selectMenu('transcription')">
        <i class="fas fa-file-alt"></i> 转写文件
      </li>
      
      <!-- 会记文件 -->
      <li :class="{ active: selectedMenu === 'meeting' }" @click="toggleSubmenu">
        <i class="fas fa-microphone"></i> 会记文件
        <i class="fas" :class="submenuOpen ? 'fa-chevron-up' : 'fa-chevron-down'" style="margin-left:auto;"></i>
      </li>
      
      <!-- 会记文件子菜单 -->
      <ul v-show="submenuOpen" class="submenu">
        <li :class="{ active: selectedSubMenu === 'recent' }" @click="selectSubMenu('recent')">
          <i class="fas fa-clock"></i> 最近文件
        </li>
        <li :class="{ active: selectedSubMenu === 'myfiles' }" @click="selectSubMenu('myfiles')">
          <i class="fas fa-folder"></i> 我的文件
        </li>
        <li :class="{ active: selectedSubMenu === 'favorites' }" @click="selectSubMenu('favorites')">
          <i class="fas fa-star"></i> 收藏文件
        </li>
        <li :class="{ active: selectedSubMenu === 'trash' }" @click="selectSubMenu('trash')">
          <i class="fas fa-trash"></i> 回收站
        </li>
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
      selectedMenu: 'transcription', // 默认选中“转写文件”
      selectedSubMenu: null,         // 追踪选中的子菜单项
    };
  },
  methods: {
    toggleSubmenu() {
      this.submenuOpen = !this.submenuOpen;
      if (this.submenuOpen) {
        this.selectedMenu = 'meeting'; // 切换时选中“会记文件”
      }
    },
    selectMenu(menu) {
      this.selectedMenu = menu;
      this.submenuOpen = menu === 'meeting'; // 选择“会记文件”时展开子菜单
    },
    selectSubMenu(subMenu) {
      this.selectedSubMenu = subMenu;
      this.selectedMenu = 'meeting'; // 保证“会记文件”处于选中状态
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
  border-radius: 0 8px 8px 0;
}

.logo-container {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
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
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 3px;
}

.menu li i {
  margin-right: 10px;
}

.menu li:hover {
  background-color: #dae7fb;
  border-radius: 8px;
}

/* 添加选中状态的样式 */
.menu li.active {
  background-color: #c3dafd;
  border-radius: 8px;
  color: #1e64ff;
}

.submenu {
  list-style-type: none;
  padding-left: 0px;
}

.submenu li {
  margin-left: 10px;
  padding: 15px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s ease;
  margin-bottom: 3px;
}

.submenu li:hover {
  background-color: #dae7fb;
  border-radius: 8px;
}

/* 子菜单选中状态样式 */
.submenu li.active {
  background-color: #c3dafd;
  border-radius: 8px;
  color: #1e64ff;
}
</style>

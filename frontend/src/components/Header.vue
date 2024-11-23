<template>
  <header class="header-container">
    <!-- 中间导航项或操作项 -->
    <div class="header-center">
      <!-- 可以放置导航链接或其他操作项 -->
    </div>

    <!-- 右侧用户信息或操作按钮 -->
    <div class="header-right">
      <!-- 示例：用户头像和下拉菜单 -->
      <div class="user-profile" @click="toggleDropdown">
        <img src="@/assets/user-avatar.jpg" alt="用户头像" class="user-avatar" />
        <span class="username">用户名</span>
        <!-- 下拉菜单 -->
        <div v-if="dropdownVisible" class="dropdown-menu">
          <ul>
            <li @click="goToProfile">个人资料</li>
            <li @click="logout">退出登录</li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      dropdownVisible: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible;
    },
    goToProfile() {
      // 跳转到个人资料页面的逻辑
      this.$router.push('/profile');
    },
    logout() {
      // 退出登录的逻辑
      alert('已退出登录');
    },
  },
};
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  height: 40px;
  background-color: #3498db;
  color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header-center {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.username {
  font-size: 16px;
}

.dropdown-menu {
  position: absolute;
  top: 60px;
  right: 0;
  background-color: white;
  color: black;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  overflow: hidden;
  z-index: 1000;
  width: 120px; /* 设置宽度，可以根据需要调整 */
}


.dropdown-menu ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-menu li {
  padding: 10px 10px;
  cursor: pointer;
}

.dropdown-menu li:hover {
  background-color: #f0f0f0;
}

</style>
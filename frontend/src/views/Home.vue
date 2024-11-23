<template>
  <div class="home">
    <!-- 侧边栏组件（固定在左侧） -->
    <Sidebar @subMenuSelected="updateFileList" />

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 录音和文件导入按钮以及搜索框 -->
      <div class="actions">
        <button @click="startRecording" class="action-button">
          <i class="fas fa-microphone"></i> 开始录制
        </button>
        <button @click="importFile" class="action-button">
          <i class="fas fa-file-import"></i> 导入文件
        </button>

        <!-- 搜索框，放在按钮右侧 -->
        <div class="search-container">
          <i class="fas fa-search search-icon"></i>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索文件"
            class="search-bar"
          />
        </div>
      </div>

      <!-- 文件列表展示，传递过滤后的文件数据给 FileList 组件 -->
      <div class="file-list-wrapper">
        <FileList :files="filteredFiles" />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue';
import FileList from '../components/FileList.vue';

export default {
  name: 'HomeView',
  components: {
    Sidebar,
    FileList
  },
  data() {
    return {
      searchQuery: '', // 搜索框输入的内容
      selectedSubMenu: null, // 当前选中的子菜单
      files: [
        { id: 1, name: '录音示例1.mp3', status: '转写完成', date: '2024/10/29', duration: '00:06' },
        { id: 2, name: '录音示例2.mp3', status: '转写完成', date: '2024/10/19', duration: '00:09' },
        { id: 3, name: '会议记录.mp3', status: '转写完成', date: '2023/11/30', duration: '14:13' },
        { id: 4, name: '示例音频.mp3', status: '转写完成', date: '2022/11/30', duration: '04:32' }
      ],
      favoriteFiles: [],  // 收藏的文件
      trashedFiles: []    // 被删除的文件
    };
  },
  computed: {
    filteredFiles() {
      let filesToShow = [];
      
      // 根据选择的子菜单来过滤文件
      if (this.selectedSubMenu === 'recent') {
        filesToShow = this.files.filter(file => {
          const fileDate = new Date(file.date);
          const oneMonthAgo = new Date();
          oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
          return fileDate >= oneMonthAgo;
        });
      } else if (this.selectedSubMenu === 'myfiles' || this.selectedMenu === 'transcription') {
        filesToShow = this.files; // 显示所有文件
      } else if (this.selectedSubMenu === 'favorites') {
        filesToShow = this.favoriteFiles; // 显示收藏的文件
      } else if (this.selectedSubMenu === 'trash') {
        filesToShow = this.trashedFiles; // 显示回收站中的文件
      } else {
        filesToShow = this.files; // 默认显示所有转写文件
      }
      
      return filesToShow.filter(file =>
        file.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    updateFileList(subMenu) {
      this.selectedSubMenu = subMenu;
    },
    // 处理录音开始
    startRecording() {
      this.$router.push('/record');
    },
    // 导入文件的逻辑
    importFile() {
      this.$router.push('/file-import');
    }
  }
};
</script>


<style scoped>
.home {
  display: flex;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 10px;
}

/* 侧边栏区域：固定在页面左侧 */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh; /* 让侧边栏占据整个页面的高度 */
  background-color: #728fda;
  color: white;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

/* 主内容区域 */
.main-content {
  margin-left: 220px; /* 给侧边栏留出空间 */
  padding: 20px;
  flex-grow: 1;
}

.actions {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.action-button {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
}

.action-button:hover {
  background-color: #357ae8;
  transform: translateY(-2px);
}

.search-container {
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 5px;
  border: 1px solid #ddd;
  padding: 5px 10px;
  gap: 5px;
}

.search-icon {
  color: #888;
  font-size: 18px;
}

.search-bar {
  width: 100%;
  border: none;
  outline: none;
  padding: 5px;
}

.file-list {
  margin-top: 20px;
}
.file-list-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  margin-top: 20px;
  max-height: calc(100vh - 170px); /* 假设顶部的固定区域高度为170px */
}
</style>

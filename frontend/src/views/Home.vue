<template>
  <div class="home">
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
    <div class="file-list">
      <FileList :files="filteredFiles" />
    </div>
  </div>
</template>

<script>
import FileList from '../components/FileList.vue'

export default {
  name: 'HomeView',
  components: {
    FileList,
  },
  data() {
    return {
      searchQuery: '', // 搜索框输入的内容
      files: [
        { id: 1, name: '录音示例1.mp3', status: '转写完成', date: '2024/10/19', duration: '00:06' },
        { id: 2, name: '录音示例2.mp3', status: '转写完成', date: '2024/10/19', duration: '00:09' },
        { id: 3, name: '会议记录.mp3', status: '转写完成', date: '2023/11/30', duration: '14:13' },
        { id: 4, name: '示例音频.mp3', status: '转写完成', date: '2022/11/30', duration: '04:32' }
      ],
    };
  },
  computed: {
    // 根据搜索框的输入过滤文件列表
    filteredFiles() {
      return this.files.filter(file =>
        file.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    // 处理录音开始
    startRecording() {
      this.$router.push('/record');
    },
    // 导入文件的逻辑
    importFile() {
      this.$router.push('/file-import');
      // alert('文件导入功能尚未实现');
    }
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 10px;
}

/* Actions区域调整布局以支持搜索框并排显示 */
.actions {
  display: flex;
  align-items: center; /* 垂直居中 */
  gap: 15px; /* 元素之间的间距 */
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

/* 搜索框样式 */
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
</style>

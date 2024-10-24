<template>
  <div class="home">
    <!-- 录音和文件导入按钮 -->
    <div class="actions">
      <button @click="startRecording" class="action-button">
        <i class="fas fa-microphone"></i> 开始录制
      </button>
      <button @click="importFile" class="action-button">
        <i class="fas fa-file-import"></i> 导入文件
      </button>
      <input type="text" v-model="searchQuery" placeholder="搜索文件..." class="search-bar" />
    </div>

    <!-- 文件列表展示 -->
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
      files: [          // 示例文件列表
        { name: '录音示例1.mp3', status: '已完成', date: '2024/10/19', duration: '00:06' },
        { name: '录音示例2.mp3', status: '已完成', date: '2024/10/19', duration: '00:09' },
        { name: '会议记录.mp3', status: '已完成', date: '2023/11/30', duration: '14:13' },
        { name: '示例音频.mp3', status: '已完成', date: '2022/11/30', duration: '04:32' }
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
      // 可以在这里添加逻辑来控制页面跳转到录制页面
      this.$router.push('/record');
    },
    // 导入文件的逻辑
    importFile() {
      // 在这里实现文件导入的功能
      alert('文件导入功能尚未实现');
    }
  }
};
</script>

<style scoped>
/* 样式可以根据你的需求进行调整 */
.home {
  padding: 20px;
  background-color: #f5f7fa;
}

.search-bar {
  padding: 10px;
  width: 250px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.actions {
  display: flex;
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
  transition: background-color 0.3s;
}

.action-button i {
  margin-right: 8px;
}

.action-button:hover {
  background-color: #357ae8;
}

.file-list {
  margin-top: 20px;
}
</style>
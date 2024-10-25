<template>
    <div class="file-list">
      <div class="file-table">
        <div class="file-item" v-for="file in filteredFiles" :key="file.id">
          <div class="file-info">
            <p>{{ file.name }}</p>
            <p>{{ file.status }}</p>
          </div>
          <div class="file-date">{{ file.date }}</div>
          <button @click="viewFile(file.id)">查看结果</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FileList',
    data() {
      return {
        searchQuery: '',
        files: [
          { id: 1, name: '某会议录音1.mp3', status: '转写完成', date: '2024/10/19 18:40' },
          { id: 2, name: '某会议音频2.mp3', status: '转写完成', date: '2024/10/19 18:41' },
          // 更多文件数据...
        ],
      };
    },
    computed: {
      filteredFiles() {
        // 根据搜索关键字筛选文件
        return this.files.filter(file => 
          file.name.includes(this.searchQuery)
        );
      },
    },
    methods: {
      viewFile(id) {
        // 查看文件结果
        alert(`查看文件ID: ${id}`);
      },
    },
  };
  </script>
  
  <style scoped>
.file-list {
  padding: 20px;
}

.file-table {
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 10px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
}

.file-item:hover {
  background-color: #f0f0f0; /* 悬停效果 */
}

.file-info {
  display: flex;
  flex-direction: column;
}

.file-date {
  font-size: 0.9em;
  color: gray;
}
</style>

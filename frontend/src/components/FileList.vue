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
          { id: 1, name: '星贡区兴园路5号', status: '转写完成', date: '2024/10/19 18:40' },
          { id: 2, name: '某会议音频.mp3', status: '转写完成', date: '2024/10/19 18:41' },
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
  
  
  .search-bar input {
    width: 200px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
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
  }
  </style>
  
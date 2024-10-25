<template>
  <div class="file-list">
    <div class="file-table">
      <div class="file-item" v-for="file in files" :key="file.id">
        <div class="file-info">
          <p>{{ file.name }}</p>
          <p :class="{'status-complete': file.status === '转写完成', 
                      'status-pending': file.status === '待处理',
                      'status-inprogress': file.status === '进行中'}">
            {{ file.status }}
          </p>
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
  props: {
    files: {
      type: Array,
      required: true,
    },
  },
  methods: {
    viewFile(id) {
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
  margin-bottom: 20px; /* 增加下方的外边距 */
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
  gap: 10px; /* 增加内容之间的间距 */
}

.file-item:hover {
  background-color: #e8f0fe; /* 悬停效果改为浅蓝色 */
}

.file-info {
  display: flex;
  flex-direction: column;
}

.file-date {
  font-size: 0.9em;
  color: #6c757d; /* 使用灰色字体 */
}

button {
  background-color: #4285f4;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

button:hover {
  background-color: #357ae8;
  transform: scale(1.05); /* 鼠标悬停效果改为放大 */
}

button:focus {
  outline: none;
}

/* 不同状态的颜色样式 */
.status-complete {
  color: #34a853; /* 转写完成为绿色 */
}

.status-pending {
  color: #ea4335; /* 待处理状态为红色 */
}

.status-inprogress {
  color: #fbbc05; /* 进行中状态为黄色 */
}
</style>

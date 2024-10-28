<template>
  <div class="file-import">
    <!-- 顶部返回按钮 -->
    <div class="header">
      <button @click="goBack" class="back-button">返回</button>
      <h2>导入文件</h2>
    </div>

    <!-- 文件导入控制 -->
    <div class="controls">
      <label class="file-input-label control-button">
        选择文件
        <input type="file" @change="handleFileUpload" class="file-input" />
      </label>
      <button @click="importFile" class="control-button">导入</button>
    </div>

    <!-- 显示导入状态 -->
    <div v-if="importStatus" class="status">
      <p>{{ importStatus }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileImport',
  data() {
    return {
      importStatus: '',
      selectedFile: null,
      transcription: '', // 存储转录结果
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    // 从文件输入中获取选择的文件，并更新状态
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.importStatus = `选择的文件: ${file.name}`;
      }
    },
    // 导入文件并发送请求到 Whisper 模型
    importFile() {
      if (this.selectedFile) {
        // 在这里添加实际的文件导入逻辑
        this.importStatus = `文件 "${this.selectedFile.name}" 已成功导入！`;
      } else {
        this.importStatus = '请先选择一个文件。';
      }
    },
  },
};
</script>

<style scoped>
.file-import {
  padding: 20px;
  background-color: #ecf4ff;
  text-align: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-button {
  padding: 8px 12px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  justify-content: center; /* 居中对齐 */
  gap: 20px; /* 增加按钮之间的间距 */
}

.file-input-label {
  display: inline-block;
  cursor: pointer;
  position: relative;
}

.file-input {
  display: none; /* 隐藏默认文件输入框 */
}

.control-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.control-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.transcription-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 20px;
}

.transcription-card h3 {
  margin-bottom: 10px;
}

.transcription-card p {
  white-space: pre-wrap; /* 保持换行 */
  line-height: 1.5; /* 增加行间距 */
}
</style>

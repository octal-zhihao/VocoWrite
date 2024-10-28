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
      <button @click="showLanguageSelection" class="control-button">导入</button>
    </div>

    <!-- 显示导入状态 -->
    <div v-if="importStatus" class="status">
      <p>{{ importStatus }}</p>
    </div>

    <!-- 显示转录结果 -->
    <div v-if="transcription" class="transcription-card">
      <h3>转录结果:</h3>
      <pre class="transcription">{{ transcription }}</pre>  <!-- 使用 <pre> 标签保留换行格式 -->
      
      <!-- 导出按钮 -->
      <div class="export-buttons">
        <button @click="exportTranscription('txt')" class="export-button">导出为 TXT</button>
        <button @click="exportTranscription('docx')" class="export-button">导出为 DOCX</button>
        <button @click="exportTranscription('md')" class="export-button">导出为 MD</button>
      </div>
    </div>

    <!-- 语言选择弹窗 -->
    <div v-if="showLanguage" class="language-modal">
      <h3>选择音频语言</h3>
      <button @click="importFile('chinese')" class="control-button">中文</button>
      <button @click="importFile('english')" class="control-button">英文</button>
      <button @click="showLanguage = false" class="control-button">取消</button>
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
      showLanguage: false, // 控制语言选择弹窗的显示
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.importStatus = `选择的文件: ${file.name}`;
      }
    },
    showLanguageSelection() {
      if (this.selectedFile) {
        this.showLanguage = true; // 显示语言选择弹窗
      } else {
        this.importStatus = '请先选择一个文件。';
      }
    },
    async importFile(language) {
      this.showLanguage = false; // 立即关闭弹窗
      if (this.selectedFile) {
        this.importStatus = `正在转录文件 "${this.selectedFile.name}"...`;
        
        const formData = new FormData();
        formData.append('audio', this.selectedFile); // 将音频文件添加到 FormData
        formData.append('language', language); // 添加语言选择

        try {
          const response = await fetch('http://127.0.0.1:8000/transcribe/api/', {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            const data = await response.json();
            this.transcription = data.transcription; // 假设返回的 JSON 包含转录结果
            this.importStatus = '文件转录完成！';
          } else {
            this.importStatus = '转录失败，请重试。';
          }
        } catch (error) {
          console.error('转录过程中出现错误: ', error);
          this.importStatus = '发生错误，请检查控制台。';
        }
      }
    },
    exportTranscription(format) {
      let blob;
      const filename = `transcription.${format}`;
      
      switch (format) {
        case 'txt':
          blob = new Blob([this.transcription], { type: 'text/plain' });
          break;
        case 'docx':
          const docxHeader = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',
            '<w:body>',
            '<w:p><w:r><w:t>' + this.transcription.replace(/\n/g, '</w:t></w:r><w:r><w:t>') + '</w:t></w:r></w:p>',
            '</w:body>',
            '</w:document>'
          ].join('');
          blob = new Blob([docxHeader], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
          break;
        case 'md':
          blob = new Blob([this.transcription], { type: 'text/markdown' });
          break;
        default:
          console.error('不支持的导出格式');
          return;
      }

      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      link.click();
      window.URL.revokeObjectURL(link.href);
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
    justify-content: center;
    gap: 20px;
  }

  .file-input-label {
    display: inline-block;
    cursor: pointer;
    position: relative;
  }

  .file-input {
    display: none;
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
    text-align: left;  /* 使转录结果左对齐 */
  }

  .transcription-card h3 {
    margin-bottom: 10px;
  }

  .transcription-card pre {
    white-space: pre-wrap; /* 保留换行 */
    line-height: 1.5;
    text-align: left; /* 使文本左对齐 */
  }

  .language-modal {
    display: flex;
    flex-direction: column;
    gap: 15px;
    position: absolute;
    top: 100px;
    right: 300px;
    background-color: white;
    padding: 20px;
    width: 200px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    z-index: 1000;
    text-align: center;
  }
  .export-buttons {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    gap: 10px;
  }

.export-button {
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>

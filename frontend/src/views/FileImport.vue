<template>
  <div class="file-import">
    <!-- 顶部返回按钮 -->
    <div class="header">
      <button @click="goBack" class="back-button">返回</button>
      <h2>导入本地会议音频</h2>
    </div>

    <!-- 文件导入控制 -->
    <div class="controls">
      <label class="file-input-label control-button">
        选择文件
        <input type="file" @change="handleFileUpload" class="file-input" />
      </label>
      <button @click="showLanguageSelection" class="control-button">导入</button>
      <button @click="generateSummary" class="control-button">生成总结</button>
    </div>

    <!-- 显示导入状态 -->
    <div v-if="importStatus" class="status">
      <p>{{ importStatus }}</p>
    </div>
    <!-- 进度条 -->
    <div v-if="isProcessing" class="progress-container">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>

    <!-- 转录结果和总结标签切换 -->
    <div v-if="transcription" class="transcription-card">
      <div class="tabs">
        <button :class="{ active: activeTab === 'transcription' }" @click="activeTab = 'transcription'">转录结果</button>
        <button :class="{ active: activeTab === 'summary' }" @click="activeTab = 'summary'">总结结果</button>
      </div>

      <!-- 转录内容 -->
      <div v-if="activeTab === 'transcription'">
        <div class="export-buttons">
          <button @click="exportTranscription('txt')" class="export-button">导出为 TXT</button>
          <button @click="exportTranscription('docx')" class="export-button">导出为 DOCX</button>
          <button @click="exportTranscription('md')" class="export-button">导出为 MD</button>
        </div>
        <pre class="transcription">
          <template v-if="selectedLanguage === 'chinese'">
            <div v-for="(sentence, index) in filteredOriginalSentences" :key="index" class="sentence">
              <div>{{ sentence + "。" }}</div>
            </div>
          </template>
          <template v-else>
            <div v-for="(sentence, index) in filteredOriginalSentences" :key="index" class="sentence">
              <div v-if="sentence.trim() !== ''">{{ sentence + "."}}</div>
              <div v-if="translatedSentences[index] && translatedSentences[index].trim() !== ''">
                {{ translatedSentences[index] + "。"}} <!-- 显示对应的中文翻译 -->
              </div>
            </div>
          </template>
        </pre>
      </div>

      <!-- 总结内容 -->
      <div v-if="activeTab === 'summary'">
        <div class="export-buttons">
          <button @click="exportSummary('txt')" class="export-button">导出为 TXT</button>
          <button @click="exportSummary('docx')" class="export-button">导出为 DOCX</button>
          <button @click="exportSummary('md')" class="export-button">导出为 MD</button>
        </div>
        <div class="summary">
          <!-- 这里展示生成的总结 -->
          <p>{{ summary }}</p>
        </div>
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
import axios from 'axios';
export default {
  name: 'FileImport',
  data() {
    return {
      importStatus: '',
      selectedFile: null,
      selectedLanguage: '', // 存储用户选择的语言
      transcription: '', // 存储转录结果
      translatedTranscription: '', // 存储翻译后的转录结果
      showLanguage: false, // 控制语言选择弹窗的显示
      originalSentences: [], // 存储原始转录结果的句子
      translatedSentences: [], // 存储翻译后的句子
      activeTab: 'transcription', // 当前选中的标签
      summary: '', // 摘要内容
      isProcessing: false, // 进度条控制
      progress: 0 // 进度值
    };
  },
  computed: {
    filteredOriginalSentences() {
      return this.originalSentences.filter(sentence => sentence.trim() !== '');
    }
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
        this.showLanguage = true;
      } else {
        this.importStatus = '请先选择一个文件。';
      }
    },
    async importFile(language) {
      this.showLanguage = false;
      if (this.selectedFile) {
        this.importStatus = `正在转录文件 "${this.selectedFile.name}"...`;
        this.selectedLanguage = language;
        const formData = new FormData();
        formData.append('audio', this.selectedFile); // 将音频文件添加到 FormData
        formData.append('language', language); // 添加语言选择

        this.isProcessing = true;
        this.progress = 0;
        const interval = setInterval(() => {
          if (this.progress < 90) {
            this.progress += 10; // 每次增加10%
          }
        }, 700);
        try {
          const response = await fetch('http://127.0.0.1:8000/transcribe/api/', {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            const data = await response.json();
            this.transcription = data.transcription;
            this.importStatus = '会议转录完成！';
            clearInterval(interval); // 完成后停止进度条
            this.isProcessing = false;
            
            if (language == 'english') {
              this.originalSentences = this.transcription.split('.').map(sentence => sentence.trim());
              // 调用翻译 API
              await this.translate();
            } else {
              this.originalSentences = this.transcription.split('。').map(sentence => sentence.trim());
            }
          } else {
            this.importStatus = '转录失败，请重试。';
          }
        } catch (error) {
          console.error('转录过程中出现错误: ', error);
          this.importStatus = '发生错误，请检查控制台。';
        } finally {
          clearInterval(interval); // 完成后停止进度条
          this.isProcessing = false;
        }
      }
    },
    async translate() {
      this.translatedSentences = [];
      try {
        let response = await fetch('http://127.0.0.1:8000/translate/api/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ texts: this.originalSentences }),  // 发送所有句子
        });

        if (response.ok) {
          const translatedData = await response.json();
          this.translatedSentences = translatedData.translated_texts;  // 批量处理结果
          this.translatedtranscription = this.translatedSentences.join('');
        } else {
          console.error('翻译失败:', response.statusText);
        }
      } catch (error) {
        console.error('翻译过程中出现错误:', error);
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
            '<w:p><w:r><w:t>' + this.transcription.replace(/\n/g, '</w:t></w:r><w:r><w:t>') + '</w:t></r></w:p>',
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

    exportSummary(format) {
      let blob;
      const filename = `summary.${format}`;

      switch (format) {
        case 'txt':
          blob = new Blob([this.summary], { type: 'text/plain' });
          break;
        case 'docx':
          const docxHeader = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',
            '<w:body>',
            '<w:p><w:r><w:t>' + this.summary.replace(/\n/g, '</w:t></w:r><w:r><w:t>') + '</w:t></r></w:p>',
            '</w:body>',
            '</w:document>'
          ].join('');
          blob = new Blob([docxHeader], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
          break;
        case 'md':
          blob = new Blob([this.summary], { type: 'text/markdown' });
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

    generateSummary() {
      this.isProcessing = true;
      this.progress = 0;

      const interval = setInterval(() => {
        if (this.progress < 90) {
          this.progress += 10; // 每次增加10%
        }
      }, 700);
      axios.post('http://127.0.0.1:8000/summarize/api/', {
        text: this.selectedLanguage === 'chinese' ? this.transcription : this.translatedtranscription
      })
      .then(response => {
        if (response.status === 200) {
          this.summary = "会议总结：" + response.data.summary;
          this.importStatus = '会议总结完成！';
        } else {
          console.error('总结生成失败:', response.status, response.data);
        }
      })
      .catch(error => {
        console.error('请求失败:', error);
      })
      .finally(() => {
        this.isProcessing = false;
      });
    }

  }
};
</script>

<style scoped>
.file-import {
  padding: 20px;
  height: 90vh;
  background-color: #ecf4ff;
  text-align: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.back-button {
  padding: 12px 20px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2em;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #357ae8;
}

.back-button i {
  font-size: 1.5em;
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
  padding: 12px 20px;
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.2em;
}

.control-button:hover {
  background-color: #357ae8;
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
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  width: 200px;
}

.language-modal h3 {
  text-align: center;
}

.export-buttons {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-around;
}

.export-button {
  background-color: #00c853;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.transcription-card {
  text-align: left;
}

.transcription {
  white-space: pre-line;
  font-size: 1.2em;
  color: #333;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 5px;
  overflow-y: auto;
  max-height: 300px; /* 设置最大高度 */
  height: auto; /* 允许内容自适应高度 */
}
.sentence {
  margin: -10px 0;  /* 调整每行之间的间距 */
  line-height: 1.3; /* 设置行间距，减少此值会使行间距更紧凑 */
}
.tabs {
  display: flex;
  justify-content: left;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  background-color: #4285f4;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1em;
  border-radius: 5px;
  margin: 0 10px;
}

.tabs button.active {
  background-color: #eb8d1b;
}

.summary {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 5px;
  border: 1px solid #ccc;
}
/* 进度条样式 */
.progress-container {
  margin: 20px auto;       /* 水平居中 */
  width: 50%;
  background-color: #f3f3f3;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 20px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(to right, #4285f4, #34a853); /* 渐变色 */
  border-radius: 10px;
  width: 0;
  transition: width 0.4s ease-out;
}

/* 导入状态样式 */
.status {
  font-size: 1.2em;
  margin-top: 20px;
}
</style>

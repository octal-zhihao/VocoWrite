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
      <div class="export-buttons">
        <button @click="exportTranscription('txt')" class="export-button">导出为 TXT</button>
        <button @click="exportTranscription('docx')" class="export-button">导出为 DOCX</button>
        <button @click="exportTranscription('md')" class="export-button">导出为 MD</button>
      </div>
      <pre class="transcription">
        <template v-if="selectedLanguage === 'chinese'">
          <div v-for="(sentence, index) in filteredOriginalSentences" :key="index" class="sentence">
            <div>{{ sentence }}</div>
          </div>
        </template>
        <template v-else>
          <div v-for="(sentence, index) in filteredOriginalSentences" :key="index" class="sentence">
            <div v-if="sentence.trim() !== ''">{{ sentence }}</div>
            <div v-if="translatedSentences[index] && translatedSentences[index].trim() !== ''">
              {{ translatedSentences[index] }} <!-- 显示对应的中文翻译 -->
            </div>
          </div>
        </template>
      </pre>
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
      selectedLanguage: '', // 存储用户选择的语言
      transcription: '', // 存储转录结果
      showLanguage: false, // 控制语言选择弹窗的显示
      bilingualTranslations: [], // 初始化双语翻译结果
      originalSentences: [], // 存储原始转录结果的句子
      translatedSentences: [] // 存储翻译后的句子
    };
  },
  computed: {
    filteredOriginalSentences() {
      // 过滤掉空行或仅有空格的行
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
        this.showLanguage = true; // 显示语言选择弹窗
      } else {
        this.importStatus = '请先选择一个文件。';
      }
    },
    async importFile(language) {
      this.showLanguage = false; // 立即关闭弹窗
      if (this.selectedFile) {
        this.importStatus = `正在转录文件 "${this.selectedFile.name}"...`;
        this.selectedLanguage = language;
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

            // 将转录文本按句子分割
            this.originalSentences = this.transcription.split('.').map(sentence => sentence.trim());

            // 调用翻译 API
            await this.translateTranscription(this.transcription);
          } else {
            this.importStatus = '转录失败，请重试。';
          }
        } catch (error) {
          console.error('转录过程中出现错误: ', error);
          this.importStatus = '发生错误，请检查控制台。';
        }
      }
    },
    async translateTranscription(transcription) {
      this.translatedSentences = []; // 清空翻译数组

      for (const sentence of this.originalSentences) {
        try {
          let response = await fetch('http://127.0.0.1:8000/translate/api/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: sentence }),
          });

          if (response.ok) {
            const translatedData = await response.json();
            const translatedSentence = translatedData.translated_text;
            this.translatedSentences.push(translatedSentence);
          } else {
            console.error('翻译失败:', response.statusText);
          }
        } catch (error) {
          console.error('翻译过程中出现错误:', error);
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
  transition: background-color 0.3s;
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
  justify-content: space-between;
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
</style>

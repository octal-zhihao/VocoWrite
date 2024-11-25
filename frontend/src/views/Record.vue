<template>
  <div class="container">
    <div class="header">
      <button @click="goBack" class="back-button">返回</button>
      <h2>会议记录</h2>
    </div>
    <div class="history">
      <div v-for="(line, index) in history" :key="index" class="history-line">
        {{ line }}
      </div>
    </div>
    <div class="controls">
      <!-- 录制按钮 -->
      <div class="tooltip-container">
        <button @click="toggleListening" class="mic-button">
          <i v-if="!listening" class="fas fa-microphone"></i>
          <i v-else class="fas fa-pause"></i>
        </button>
        <span class="tooltip-text">{{ listening ? '暂停录制' : '开始录制' }}</span>
      </div>

      <!-- 结束按钮 -->
      <div class="tooltip-container">
        <button @click="stopRecording" class="stop-button">
          <i class="fas fa-stop"></i>
        </button>
        <span class="tooltip-text">结束录制</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      history: [],
      listening: false,
      recognition: null,
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    initSpeechRecognition() {
      this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
      this.recognition.lang = 'zh-CN';
      this.recognition.continuous = true;
      this.recognition.interimResults = true;

      this.recognition.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          this.history.push(finalTranscript);
        }
      };

      this.recognition.onerror = (event) => {
        console.error('Speech recognition error:', event);
      };
    },
    toggleListening() {
      if (!this.recognition) this.initSpeechRecognition();
      if (this.listening) {
        this.recognition.stop();
      } else {
        this.recognition.start();
      }
      this.listening = !this.listening;
    },
    stopRecording() {
      if (this.listening) {
        this.recognition.stop();
        this.listening = false;
      }
      if (confirm('是否保存转写内容？')) {
        this.saveTranscription();
      }
    },
    saveTranscription() {
      const blob = new Blob([this.history.join('\n')], { type: 'text/plain' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'transcription.txt';
      link.click();
      URL.revokeObjectURL(link.href);
    },
  },
  mounted() {
    if (!('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)) {
      alert('当前浏览器不支持实时语音识别功能。');
    }
  },
};
</script>

<style scoped>

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  margin: 0;
  padding: 20px;
  background-color: #f0f4f8;
}

h1 {
  text-align: center;
  font-size: 2em;
  margin-bottom: 10px;
  color: #333;
}

.history {
  flex-grow: 1;
  overflow-y: auto;
  border-radius: 10px;
  background-color: #fff;
  padding: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 80px;
}

.history-line {
  margin-bottom: 10px;
  padding: 8px;
  background-color: #f7f7f7;
  border-radius: 5px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.controls {
  position: fixed;
  bottom: 0;
  left: 20px;
  width: 1488px;
  background-color: rgba(135, 206, 250, 0.5); /* 浅蓝色半透明背景 */
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px 0; /* 增大了内边距 */
}

.mic-button,
.stop-button {
  background-color: transparent;
  border: none;
  font-size: 2em;
  color: #333;
  cursor: pointer;
  transition: transform 0.3s;
}

.mic-button:hover,
.stop-button:hover {
  transform: scale(1.1);
}

/* Tooltip 样式 */
.tooltip-container {
  position: relative;
  display: inline-block;
}

.tooltip-text {
  visibility: hidden;
  background-color: #333;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  position: absolute;
  bottom: 100%;  /* 在按钮上方显示 */
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

.back-button {
  padding: 12px 20px;  /* 增大了按钮的内边距 */
  background-color: #4285f4;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;  /* 增大图标和文字的间距 */
  font-size: 1.2em;  /* 增大文字大小 */
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: #357ae8;  /* 增加按钮的悬浮效果 */
}

.back-button i {
  font-size: 1.5em;  /* 增大图标的大小 */
}

</style>

<template>
  <div class="record">
    <!-- 顶部返回按钮 -->
    <div class="header">
      <button @click="goBack" class="back-button">返回</button>
      <h2>录音界面</h2>
    </div>

    <!-- 录音状态和计时器 -->
    <div class="status">
      <p v-if="isPaused">录音已暂停</p>
      <p v-else>{{ isRecording ? '录音中...' : '录音已停止' }}</p>
      <p>录音时长: {{ formatTime(elapsedTime) }}</p>
    </div>

    <!-- 录音控制按钮 -->
    <div class="controls">
      <button @click="startRecording" :disabled="isRecording || isPaused" class="control-button">开始录音</button>
      <button @click="pauseRecording" :disabled="!isRecording" class="control-button">暂停录音</button>
      <button v-if="isPaused" @click="resumeRecording" class="control-button">继续录音</button>
      <button @click="stopRecording" :disabled="!isRecording && !isPaused" class="control-button">停止录音</button>
      <button @click="playRecording" :disabled="!audioUrl" class="control-button">播放录音</button>
    </div>

    <!-- 录音播放 -->
    <div v-if="audioUrl" class="audio-player">
      <audio :src="audioUrl" controls></audio>
    </div>

    <!-- 可编辑文本框 -->
    <div class="editable-section">
      <div
        contenteditable="true"
        class="paragraph-dom selectNone"
        @input="updateText"
        @focus="handleFocus"
        @blur="handleBlur"
      >
        <span class="input-text">{{ inputText }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Record',
  data() {
    return {
      mediaRecorder: null,
      audioChunks: [],
      audioUrl: null,
      isRecording: false,
      isPaused: false,
      timer: null,
      elapsedTime: 0,
      inputText: '',
      isFocused: false, 
    };
  },
  methods: {
    updateText(event) {
      this.inputText = event.target.innerText; // 更新输入文本
    },
    
    handleFocus() {
      this.isFocused = true; // 设置焦点状态为 true
    },

    handleBlur() {
      this.isFocused = false; // 设置焦点状态为 false
    },

    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    },

    goBack() {
      this.$router.go(-1);
    },

    startRecording() {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('当前浏览器不支持录音功能');
        return;
      }

      navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        this.mediaRecorder = new MediaRecorder(stream);
        this.audioChunks = [];
        this.isRecording = true;
        this.isPaused = false;
        this.elapsedTime = 0;

        this.timer = setInterval(() => {
          this.elapsedTime += 1;
        }, 1000);

        this.mediaRecorder.ondataavailable = event => {
          this.audioChunks.push(event.data);
        };

        this.mediaRecorder.onstop = () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/mp3' });
          this.audioUrl = URL.createObjectURL(audioBlob);
        };

        this.mediaRecorder.start();
      }).catch(error => {
        console.error('无法访问麦克风: ', error);
        alert('无法访问麦克风');
      });
    },

    pauseRecording() {
      if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
        this.mediaRecorder.pause();
        this.isRecording = false;
        this.isPaused = true;
        clearInterval(this.timer);
      }
    },

    resumeRecording() {
      if (this.mediaRecorder && this.mediaRecorder.state === 'paused') {
        this.mediaRecorder.resume();
        this.isRecording = true;
        this.isPaused = false;

        this.timer = setInterval(() => {
          this.elapsedTime += 1;
        }, 1000);
      }
    },

    stopRecording() {
      if (this.mediaRecorder && (this.mediaRecorder.state === 'recording' || this.mediaRecorder.state === 'paused')) {
        this.mediaRecorder.stop();
        this.isRecording = false;
        this.isPaused = false;
        clearInterval(this.timer);
      }
    },

    playRecording() {
      if (this.audioUrl) {
        const audio = new Audio(this.audioUrl);
        audio.play();
      }
    }
  }
};
</script>

<style scoped>
.record {
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

.status {
  margin-bottom: 20px;
  font-size: 1.2em;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
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

.audio-player {
  margin-top: 20px;
}

.editable-section {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #fff;
}

.paragraph-dom {
  min-height: 50px; /* 可根据需要调整 */
  padding: 5px;
  position: relative;
  text-align: left; /* 确保文本左对齐 */
}

.input-text {
  color: black; /* 设置输入文本为黑色 */
}
</style>

<template>
  <div class="record-button-container">
    <!-- 录音按钮 -->
    <button
      class="action-button"
      :class="{ 'is-recording': isRecording }"
      @click="toggleRecording"
    >
      <!-- 根据录音状态显示不同的文本 -->
      {{ isRecording ? '停止录音' : '开始录制' }}
    </button>

    <!-- 录音状态提示 -->
    <div class="recording-status" v-if="isRecording">
      录音中...
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecordButton',
  data() {
    return {
      isRecording: false,
    };
  },
  methods: {
    toggleRecording() {
      this.isRecording = !this.isRecording;
      this.$emit('start-record');
    },
  },
};
</script>

<style scoped>
.action-button {
  padding: 10px 20px;
  background-color: #4285f4; /* 统一背景颜色 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #357ae8;
}

.is-recording {
  background-color: #ff4b5c; /* 录音时的背景颜色 */
}

.recording-status {
  margin-top: 10px;
  color: #ff4b5c;
  font-weight: bold;
}
</style>
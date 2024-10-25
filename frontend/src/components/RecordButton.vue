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
.record-button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.action-button {
  padding: 15px 30px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
}

.action-button:hover {
  background-color: #c0392b; /* 鼠标悬停颜色 */
  transform: scale(1.05); /* 鼠标悬停放大效果 */
}

.recording-status {
  margin-top: 10px;
  color: #e74c3c;
  font-weight: bold;
}
</style>

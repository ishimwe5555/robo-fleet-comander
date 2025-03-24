<template>
  <div class="websocket-tester">
    <h3>WebSocket Tester</h3>
    <div class="status">
      Status: {{ connected ? '🟢 Connected' : '🔴 Disconnected' }}
    </div>
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index">
        {{ msg }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const connected = ref(false)
const messages = ref<string[]>([])
const ws = ref<WebSocket | null>(null)

onMounted(() => {
  ws.value = new WebSocket('ws://localhost:8000/ws')
  
  ws.value.onopen = () => {
    connected.value = true
    messages.value.push('Connected to WebSocket')
  }

  ws.value.onmessage = (event) => {
    messages.value.push(`Received: ${event.data}`)
  }

  ws.value.onclose = () => {
    connected.value = false
    messages.value.push('Disconnected from WebSocket')
  }
})

onUnmounted(() => {
  ws.value?.close()
})
</script>

<style scoped>
.websocket-tester {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 1rem;
}

.status {
  margin: 1rem 0;
  font-weight: bold;
}

.messages {
  max-height: 200px;
  overflow-y: auto;
  padding: 0.5rem;
  background: #f5f5f5;
}
</style> 
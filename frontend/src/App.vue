<template>
  <nav>
    <RouterLink to="/">Dashboard</RouterLink>
    <RouterLink to="/missions">Missions</RouterLink>
    <RouterLink to="/fleet">Fleet</RouterLink>
  </nav>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { wsService } from './services/websocket'

onMounted(() => {
  wsService.connect()
})

onUnmounted(() => {
  wsService.disconnect()
})
</script>

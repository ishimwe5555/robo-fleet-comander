<template>
  <div class="dashboard">
    <div class="status-panel">
      <h2>Robot Status</h2>
      <!-- Robot status cards will go here -->
    </div>
    <div id="map" class="map-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Map, View } from 'ol'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'
import { fromLonLat } from 'ol/proj'
import { useRobotStore } from '../stores/robotStore'

const robotStore = useRobotStore()

onMounted(() => {
  const map = new Map({
    target: 'map',
    layers: [
      new TileLayer({
        source: new OSM()
      })
    ],
    view: new View({
      center: fromLonLat([4.35, 50.85]), // Brussels coordinates
      zoom: 12
    })
  })
})
</script>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  height: 100vh;
}

.status-panel {
  padding: 20px;
  background: #f5f5f5;
}

.map-container {
  height: 100%;
}
</style>

<template>
  <div class="dashboard">
    <div class="status-panel">
      <h2>Robot Status</h2>
      <button @click="addTestRobot">Add Test Robot</button>
    </div>
    <div id="map" class="map-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Map, View } from 'ol'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import { Feature } from 'ol'
import { Point } from 'ol/geom'
import { Style, Circle, Fill, Stroke } from 'ol/style'
import OSM from 'ol/source/OSM'
import { fromLonLat } from 'ol/proj'
import { useRobotStore } from '../stores/robotStore'

const robotStore = useRobotStore()
const robotLayer = ref<VectorLayer<VectorSource>>()

onMounted(() => {
  // Create vector source and layer for robots
  const vectorSource = new VectorSource()
  robotLayer.value = new VectorLayer({
    source: vectorSource,
    style: new Style({
      image: new Circle({
        radius: 8,
        fill: new Fill({ color: '#ff3333' }),
        stroke: new Stroke({ color: '#ffffff', width: 2 })
      })
    })
  })

  const map = new Map({
    target: 'map',
    layers: [
      new TileLayer({
        source: new OSM()
      }),
      robotLayer.value
    ],
    view: new View({
      center: fromLonLat([4.35, 50.85]), // Brussels
      zoom: 12
    })
  })
})

// Test function to add a robot
const addTestRobot = () => {
  if (!robotLayer.value) return

  const source = robotLayer.value.getSource()
  if (!source) return

  // Create a new robot in a random position near Brussels
  const randomOffset = () => (Math.random() - 0.5) * 0.1
  const position = [4.35 + randomOffset(), 50.85 + randomOffset()]
  
  const robotFeature = new Feature({
    geometry: new Point(fromLonLat(position))
  })

  source.addFeature(robotFeature)

  // Add to store
  robotStore.robots.push({
    id: `robot-${robotStore.robots.length + 1}`,
    name: `Robot ${robotStore.robots.length + 1}`,
    status: 'active',
    position: position as [number, number]
  })
}
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

button {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #45a049;
}
</style>

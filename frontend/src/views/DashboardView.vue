<template>
  <div class="dashboard">
    <div class="status-panel">
      <h2>Robot Status</h2>
      <div v-for="robot in robotStore.robots" :key="robot.id" class="robot-status">
        <div class="robot-header">
          {{ robot.name }} - {{ robot.status }}
        </div>
        <div class="robot-controls">
          <button @click="activateRobot(robot.id)">Activate</button>
          <button @click="deactivateRobot(robot.id)">Deactivate</button>
          <div class="position">
            [{{ robot.position[0].toFixed(2) }}, {{ robot.position[1].toFixed(2) }}]
          </div>
        </div>
      </div>
      <WebSocketTester />
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
import WebSocketTester from '../components/WebSocketTester.vue'

const robotStore = useRobotStore()
const robotLayer = ref<VectorLayer<VectorSource>>()
const robotFeatures = ref<Record<string, Feature<Point>>>({})

onMounted(async () => {
  const vectorSource = new VectorSource()
  robotLayer.value = new VectorLayer({
    source: vectorSource,
    style: new Style({
      image: new Circle({
        radius: 12,  // Bigger radius
        fill: new Fill({ color: '#ff3333' }),
        stroke: new Stroke({ color: '#ffffff', width: 3 })
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
      center: fromLonLat([4.35, 50.85]), // Brussels center
      zoom: 11  // Zoom out a bit to see all robots
    })
  })

  // Fetch and add robots
  await robotStore.fetchRobots()
  console.log('Loaded robots:', robotStore.robots)

  robotStore.robots.forEach(robot => {
    console.log(`Adding robot ${robot.id} at position:`, robot.position)
    const feature = new Feature({
      geometry: new Point(fromLonLat(robot.position))
    })
    robotFeatures.value[robot.id] = feature
    robotLayer.value?.getSource()?.addFeature(feature)
  })
})

const activateRobot = async (robotId: string) => {
  try {
    const response = await fetch(`http://localhost:8000/api/robots/${robotId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'active' })
    })
    if (response.ok) {
      robotStore.updateRobotStatus(robotId, 'active')
    }
  } catch (error) {
    console.error('Error activating robot:', error)
  }
}

const deactivateRobot = async (robotId: string) => {
  try {
    const response = await fetch(`http://localhost:8000/api/robots/${robotId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'inactive' })
    })
    if (response.ok) {
      robotStore.updateRobotStatus(robotId, 'inactive')
    }
  } catch (error) {
    console.error('Error deactivating robot:', error)
  }
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

.robot-status {
  padding: 12px;
  margin: 8px 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.robot-header {
  font-weight: bold;
  margin-bottom: 8px;
}

.robot-controls {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.robot-controls button {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #4CAF50;
  color: white;
}

.robot-controls button:hover {
  background: #45a049;
}

.position {
  font-size: 0.9em;
  color: #666;
  margin-top: 4px;
  width: 100%;
}
</style>

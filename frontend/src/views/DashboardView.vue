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
import { Point, LineString } from 'ol/geom'
import { Style, Circle, Fill, Stroke } from 'ol/style'
import OSM from 'ol/source/OSM'
import { fromLonLat } from 'ol/proj'
import { useRobotStore } from '../stores/robotStore'
import WebSocketTester from '../components/WebSocketTester.vue'
import { transform } from 'ol/proj'

const robotStore = useRobotStore()
const robotLayer = ref<VectorLayer<VectorSource>>()
const robotFeatures = ref<Record<string, Feature<Point>>>({})
const trailLayers = ref<Record<string, VectorLayer<VectorSource>>>({})
const map = ref<Map>()

onMounted(async () => {
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

  map.value = new Map({
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

  // Fetch robots and add them to the map
  await robotStore.fetchRobots()

  // Add click handler
  map.value.on('click', (event) => {
    const coords = transform(event.coordinate, 'EPSG:3857', 'EPSG:4326')
    console.log('Map clicked at:', coords)  // Debug log
    
    const activeRobots = robotStore.robots.filter(r => r.status === 'active')
    console.log('Active robots:', activeRobots)  // Debug log
    
    activeRobots.forEach(robot => {
      console.log(`Moving robot ${robot.id} to ${coords[0]}, ${coords[1]}`)  // Debug log
      moveRobot(robot.id, coords[0], coords[1])
    })
  })

  robotStore.robots.forEach(robot => {
    console.log(`Adding robot ${robot.id} at position:`, robot.position)
    const feature = new Feature({
      geometry: new Point(fromLonLat(robot.position))
    })
    robotFeatures.value[robot.id] = feature
    robotLayer.value?.getSource()?.addFeature(feature)
  })

  // Update trails every 2 seconds
  setInterval(() => {
    robotStore.robots.forEach(robot => {
      if (robot.status === 'active') {
        updateRobotTrail(robot.id)
      }
    })
  }, 2000)
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

const createTrailLayer = (robotId: string) => {
  const source = new VectorSource()
  const layer = new VectorLayer({
    source,
    style: new Style({
      stroke: new Stroke({
        color: '#ff3333',
        width: 2,
        lineDash: [5, 5],
      })
    })
  })
  trailLayers.value[robotId] = layer
  map.value?.addLayer(layer)
}

const updateRobotTrail = async (robotId: string) => {
  try {
    const response = await fetch(`http://localhost:8000/api/robots/${robotId}/trail`)
    const data = await response.json()
    
    if (!trailLayers.value[robotId]) {
      createTrailLayer(robotId)
    }

    const coordinates = data.trail.map((point: any) => 
      fromLonLat([point.longitude, point.latitude])
    )

    const lineString = new LineString(coordinates)
    const feature = new Feature(lineString)
    
    const source = trailLayers.value[robotId].getSource()
    source?.clear()
    source?.addFeature(feature)
  } catch (error) {
    console.error('Error updating trail:', error)
  }
}

const moveRobot = async (robotId: string, longitude: number, latitude: number) => {
  try {
    const response = await fetch(
      `http://localhost:8000/api/robots/${robotId}/move?target_longitude=${longitude}&target_latitude=${latitude}`,
      {
        method: 'POST'
      }
    )
    const data = await response.json()
    console.log('Move response:', data)  // Debug log
  } catch (error) {
    console.error('Error moving robot:', error)
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

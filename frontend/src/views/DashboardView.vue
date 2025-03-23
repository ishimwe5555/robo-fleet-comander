<template>
  <div class="dashboard">
    <div class="status-panel">
      <h2>Robot Status</h2>
      <button @click="addTestRobot">Add Robot</button>
      <button @click="startMoving">Start Moving</button>
      <button @click="stopMoving">Stop</button>
      <button @click="clearPaths">Clear Paths</button>
    </div>
    <div id="map" class="map-container"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted } from 'vue'
import { Map, View } from 'ol'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import { Feature } from 'ol'
import { Point } from 'ol/geom'
import LineString from 'ol/geom/LineString'
import { Style, Circle, Fill, Stroke } from 'ol/style'
import OSM from 'ol/source/OSM'
import { fromLonLat, toLonLat } from 'ol/proj'
import { useRobotStore } from '../stores/robotStore'

const robotStore = useRobotStore()
const robotLayer = ref<VectorLayer<VectorSource>>()
const pathLayer = ref<VectorLayer<VectorSource>>()
const robotFeatures = ref<Record<string, Feature<Point>>>({})
const robotPaths = ref<Record<string, Feature<LineString>>>({})
const animationFrameId = ref<number>()

// Movement parameters
const SPEED = 0.0005 // degrees per frame
const isMoving = ref(false)

onMounted(() => {
  // Create path layer
  const pathSource = new VectorSource()
  pathLayer.value = new VectorLayer({
    source: pathSource,
    style: new Style({
      stroke: new Stroke({
        color: '#ff333380',
        width: 2
      })
    })
  })

  // Create robot layer
  const robotSource = new VectorSource()
  robotLayer.value = new VectorLayer({
    source: robotSource,
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
      pathLayer.value,  // Add paths under robots
      robotLayer.value
    ],
    view: new View({
      center: fromLonLat([4.35, 50.85]),
      zoom: 12
    })
  })
})

const addTestRobot = () => {
  if (!robotLayer.value) return
  const source = robotLayer.value.getSource()
  if (!source) return

  const randomOffset = () => (Math.random() - 0.5) * 0.1
  const position = [4.35 + randomOffset(), 50.85 + randomOffset()]
  const projectedPosition = fromLonLat(position)
  
  const robotId = `robot-${robotStore.robots.length + 1}`
  
  // Create robot marker
  const robotFeature = new Feature({
    geometry: new Point(projectedPosition)
  })
  source.addFeature(robotFeature)
  robotFeatures.value[robotId] = robotFeature

  // Create path feature
  const pathFeature = new Feature({
    geometry: new LineString([projectedPosition])
  })
  pathLayer.value?.getSource()?.addFeature(pathFeature)
  robotPaths.value[robotId] = pathFeature

  robotStore.robots.push({
    id: robotId,
    name: `Robot ${robotStore.robots.length + 1}`,
    status: 'active',
    position: position as [number, number]
  })
}

const moveRobots = () => {
  console.log('Moving robots...')
  Object.entries(robotFeatures.value).forEach(([robotId, feature]) => {
    const geometry = feature.getGeometry() as Point
    const coords = geometry.getCoordinates()
    
    const angle = Math.random() * Math.PI * 2
    const dx = Math.cos(angle) * SPEED
    const dy = Math.sin(angle) * SPEED
    
    const [lon, lat] = toLonLat(coords)
    console.log(`Robot ${robotId} moving to:`, lon + dx, lat + dy)
    
    const newPosition = fromLonLat([lon + dx, lat + dy])
    geometry.setCoordinates(newPosition)
    
    // Update path
    const pathFeature = robotPaths.value[robotId]
    if (pathFeature) {
      const path = pathFeature.getGeometry() as LineString
      const coordinates = path.getCoordinates()
      coordinates.push(newPosition)
      path.setCoordinates(coordinates)
    }
    
    const robot = robotStore.robots.find(r => r.id === robotId)
    if (robot) {
      robot.position = [lon + dx, lat + dy]
    }
  })

  if (isMoving.value) {
    animationFrameId.value = requestAnimationFrame(moveRobots)
  }
}

const startMoving = () => {
  console.log('Starting movement...') // Debug log
  isMoving.value = true
  moveRobots()
}

const stopMoving = () => {
  isMoving.value = false
  if (animationFrameId.value) {
    cancelAnimationFrame(animationFrameId.value)
  }
}

const clearPaths = () => {
  Object.values(robotPaths.value).forEach(pathFeature => {
    const geometry = pathFeature.getGeometry() as LineString
    // Reset path to current robot position
    const robotPosition = geometry.getCoordinates().slice(-1)
    geometry.setCoordinates(robotPosition)
  })
}

// Cleanup
onUnmounted(() => {
  if (animationFrameId.value) {
    cancelAnimationFrame(animationFrameId.value)
  }
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
  display: flex;
  flex-direction: column;
  gap: 10px;
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

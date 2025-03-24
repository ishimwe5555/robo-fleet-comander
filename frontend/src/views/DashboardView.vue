<template>
  <div class="dashboard">
    <div class="status-panel">
      <h2>Robot Status</h2>
      <div v-for="robot in robotStore.robots" :key="robot.id" class="robot-status">
        {{ robot.name }} - {{ robot.status }}
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
  padding: 8px;
  margin: 4px 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>

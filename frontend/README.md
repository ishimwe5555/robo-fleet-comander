# 🤖 RoboFleet Commander - Frontend

The Vue.js frontend for our robot fleet management dashboard. Watch robots move in real-time, track their paths, and control their missions!

## ✨ Features

- 🗺️ Interactive map with OpenLayers
- 📍 Real-time robot position tracking
- 🛣️ Path visualization
- 🎮 Robot control interface

## 🛠️ Tech Stack

- Vue 3
- TypeScript
- OpenLayers for mapping
- Pinia for state management
- Vite for development

## 🚀 Getting Started

### Setup
```sh
npm install
```

### Development
```sh
npm run dev
```

### Production Build
```sh
npm run build
```

## 💻 Recommended IDE Setup

- [VSCode](https://code.visualstudio.com/) 
- [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur)

## 📁 Project Structure

```
src/
├── views/              # Main view components
│   ├── DashboardView   # Main robot tracking interface
│   ├── MissionsView    # Mission planning (coming soon)
│   └── FleetView       # Fleet management
├── stores/             # Pinia state management
│   └── robotStore      # Robot state and actions
├── components/         # Reusable components
└── router/             # Vue router configuration
```

## 🎯 Current Status

- ✅ Basic map interface
- ✅ Robot movement simulation
- ✅ Path tracking
- 🚧 Mission planning
- 🚧 Backend integration

---
*Part of the RoboFleet Commander project - Making robot fleet management fun!*

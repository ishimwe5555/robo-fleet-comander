# 🤖 RoboFleet Commander

A real-time robot fleet management system with interactive mapping and WebSocket communication.

## ✨ Features

### Current Features
- 🗺️ Interactive OpenLayers map interface
- 🤖 Real-time robot position tracking
- 🔄 WebSocket-based live updates
- 🎮 Robot controls:
  - Activate/Deactivate robots
  - Move robots by clicking on map
  - Stop robot movement
- 📍 Status monitoring panel

### Planned Features
- 🛣️ Path visualization and trails
- 📝 Mission planning and waypoints
- 🔋 Robot status simulation (battery, speed, etc.)
- 🎯 Zone mapping and boundaries

## 🛠️ Tech Stack

### Frontend
- Vue 3 with TypeScript
- Pinia for state management
- OpenLayers for mapping
- WebSocket for real-time updates

### Backend
- FastAPI
- SQLAlchemy
- SQLite database
- WebSocket for real-time communication

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
bash
cd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend Setup
bash
cd frontend
npm install
npm run dev

### Default Ports
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

## 🎮 Usage

1. Start both backend and frontend servers
2. Open http://localhost:5173 in your browser
3. Create robots using the API:
   ```bash
   curl -X POST "http://localhost:8000/api/robots?name=TestBot"
   ```
4. Activate robots using the dashboard controls
5. Click on the map to move active robots
6. Monitor real-time updates in the status panel

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
Built with ❤️ for robot fleet management enthusiasts
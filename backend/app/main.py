from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .routes import robots
from .models.robot import Base
from .database import engine
from .websocket.connection import manager

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RoboFleet Commander API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(robots.router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to RoboFleet Commander API"}

@app.get("/api/robots")
async def get_robots():
    # Temporary mock data
    return {
        "robots": [
            {
                "id": "robot-1",
                "name": "Explorer-1",
                "status": "active",
                "position": [4.35, 50.85]  # Brussels coordinates
            }
        ]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await manager.broadcast(f"Message text was: {data}")
    except:
        manager.disconnect(websocket) 
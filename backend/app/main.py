from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RoboFleet Commander API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
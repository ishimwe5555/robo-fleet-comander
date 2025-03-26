from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.robot import Robot, TrailPoint
from ..websocket.connection import manager
from ..simulation.movement import movement_simulator
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()

class StatusUpdate(BaseModel):
    status: str

@router.get("/robots")
async def get_robots(db: Session = Depends(get_db)):
    robots = db.query(Robot).all()
    return {"robots": robots}

@router.post("/robots")
async def create_robot(name: str, db: Session = Depends(get_db)):
    robot = Robot(
        id=f"robot-{name.lower()}",
        name=name,
        status="inactive",
        latitude=50.85,
        longitude=4.35
    )
    db.add(robot)
    db.commit()
    db.refresh(robot)
    return robot

@router.put("/robots/{robot_id}/position")
async def update_robot_position(
    robot_id: str, 
    latitude: float, 
    longitude: float,
    db: Session = Depends(get_db)
):
    robot = db.query(Robot).filter(Robot.id == robot_id).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    
    robot.latitude = latitude
    robot.longitude = longitude
    db.commit()

    # Broadcast position update
    await manager.broadcast_robot_position(
        robot_id, 
        {"latitude": latitude, "longitude": longitude}
    )
    
    return {"status": "success"}

@router.put("/robots/{robot_id}/status")
async def update_robot_status(
    robot_id: str,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    robot = db.query(Robot).filter(Robot.id == robot_id).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    
    robot.status = status_update.status
    db.commit()
    
    # Broadcast status update through WebSocket
    await manager.broadcast({
        "type": "status_update",
        "robot_id": robot_id,
        "status": status_update.status
    })
    
    return {"status": "success"}

@router.get("/robots/{robot_id}/trail")
def get_robot_trail(
    robot_id: str,
    minutes: int = 30,
    db: Session = Depends(get_db)
):
    time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
    trail_points = db.query(TrailPoint).filter(
        TrailPoint.robot_id == robot_id,
        TrailPoint.timestamp >= time_threshold
    ).order_by(TrailPoint.timestamp).all()
    
    return {
        "trail": [
            {
                "longitude": point.longitude,
                "latitude": point.latitude,
                "timestamp": point.timestamp
            } for point in trail_points
        ]
    } 

@router.post("/robots/{robot_id}/move")
async def move_robot(
    robot_id: str,
    target_longitude: float,
    target_latitude: float,
    db: Session = Depends(get_db)
):
    print(f"Moving robot {robot_id} to: {target_longitude}, {target_latitude}")
    robot = db.query(Robot).filter(Robot.id == robot_id).first()
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    
    if robot.status != "active":
        raise HTTPException(status_code=400, detail="Robot must be active to move")

    movement_simulator.start_robot_movement(
        robot_id,
        (robot.longitude, robot.latitude),
        (target_longitude, target_latitude)
    )
    
    return {"status": "movement started"} 
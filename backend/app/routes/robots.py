from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.robot import Robot
from ..websocket.connection import manager
from pydantic import BaseModel

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
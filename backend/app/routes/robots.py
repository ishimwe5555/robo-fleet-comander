from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.robot import Robot

router = APIRouter()

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
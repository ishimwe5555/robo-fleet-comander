from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default="inactive")
    latitude = Column(Float)
    longitude = Column(Float)
    trail_points = relationship("TrailPoint", back_populates="robot", order_by="TrailPoint.timestamp")

class TrailPoint(Base):
    __tablename__ = "trail_points"

    id = Column(Integer, primary_key=True)
    robot_id = Column(String, ForeignKey('robots.id'))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    robot = relationship("Robot", back_populates="trail_points") 
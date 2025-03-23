from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, default="inactive")
    latitude = Column(Float)
    longitude = Column(Float) 
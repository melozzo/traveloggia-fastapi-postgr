from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from database import Base
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Device properties
    devicename = Column(String(255), nullable=True)
    devicetype = Column(String(100), nullable=True)
    devicetoken = Column(String(500), nullable=True)
    memberid = Column(Integer, nullable=True, index=True)
    daterecorded = Column(DateTime, default=datetime.now)

    # Add other Device columns based on your actual table structure:
    # platform = Column(String(50), nullable=True)  # iOS, Android, etc.
    # appversion = Column(String(20), nullable=True)
    # isactive = Column(Boolean, default=True)
    # lastused = Column(DateTime, nullable=True)
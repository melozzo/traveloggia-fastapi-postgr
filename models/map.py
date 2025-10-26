from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Map(Base):
    __tablename__ = "maps"

    # Primary key
    mapid = Column(Integer, primary_key=True, index=True)

    # Map properties
    mapname = Column(String(255), nullable=True)
    memberid = Column(Integer, nullable=False, index=True)  # Foreign key to Members
    createdate = Column(DateTime, default=datetime.now)
    lastrevision = Column(DateTime, nullable=True)

    # Boolean flags
    isdeleted = Column(Boolean, default=False)
    crowdsourced = Column(Boolean, default=False)
    fromphone = Column(Boolean, default=False)
    haslayers = Column(Boolean, default=False)

    # Relationship to Sites (one-to-many)
    sites = relationship("Site", back_populates="map", cascade="all, delete-orphan")


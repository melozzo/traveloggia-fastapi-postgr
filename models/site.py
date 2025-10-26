from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from typing import Optional
from datetime import datetime

class Site(Base):
    __tablename__ = "sites"

    siteid = Column(Integer, primary_key=True, index=True)
    mapid = Column(Integer, ForeignKey("maps.mapid"), nullable=False)
    name = Column(String, nullable=True)
    from sqlalchemy import DECIMAL
    longitude = Column(DECIMAL, nullable=True)
    latitude = Column(DECIMAL, nullable=True)
    memberid = Column(Integer, nullable=True)
    address = Column(String, nullable=True)
    description = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    url = Column(String, nullable=True)
    fromphone = Column(Boolean, nullable=True)
    rating = Column(Integer, nullable=True)
    averagerating = Column(DECIMAL, nullable=True)
    votescast = Column(Integer, nullable=True)
    departure = Column(DateTime, nullable=True)
    routeindex = Column(Integer, nullable=True)
    arrival = Column(DateTime, nullable=True)
    isdeleted = Column(Boolean, default=False)
    dateadded = Column(DateTime, default=datetime.utcnow)

    # Relationship to Map (optional, if you want to use it)
    map = relationship("Map", back_populates="sites")

    # Relationship to Photo (one-to-many)
    photos = relationship("Photo", back_populates="site", cascade="all, delete-orphan")

    # Relationship to Journal (one-to-many)
    journals = relationship("Journal", back_populates="site", cascade="all, delete-orphan")

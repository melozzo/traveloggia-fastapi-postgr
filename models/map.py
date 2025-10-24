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

class Site(Base):
    __tablename__ = "sites"

    # Primary key
    siteid = Column(Integer, primary_key=True, index=True)

    # Foreign key to Map
    mapid = Column(Integer, ForeignKey("maps.mapid"), nullable=False, index=True)

    # Site properties
    sitename = Column(String(255), nullable=True)
    routeindex = Column(Integer, nullable=True)
    arrival = Column(DateTime, nullable=True)
    dateadded = Column(DateTime, default=datetime.now)  # Added from controller
    isdeleted = Column(Boolean, default=False)

    # Add other Site columns based on your actual table structure:
    # latitude = Column(Float, nullable=True)
    # longitude = Column(Float, nullable=True)
    # description = Column(Text, nullable=True)

    # Relationship back to Map (many-to-one)
    map = relationship("Map", back_populates="sites")

    # Relationships to Photos and Journals (referenced in DeleteSite)
    photos = relationship("Photo", back_populates="site", cascade="all, delete-orphan")
    journals = relationship("Journal", back_populates="site", cascade="all, delete-orphan")
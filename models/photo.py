from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Photo(Base):
    __tablename__ = "photos"

    # Primary key
    photoid = Column(Integer, primary_key=True, index=True)

    # Foreign key to Site
    siteid = Column(Integer, ForeignKey("sites.siteid"), nullable=False, index=True)

    # Photo properties
    photoname = Column(String(255), nullable=True)
    photopath = Column(String(500), nullable=True)
    datetaken = Column(DateTime, nullable=True)
    dateadded = Column(DateTime, default=datetime.now)
    isdeleted = Column(Boolean, default=False)

    # Add other Photo columns based on your actual table structure:
    # caption = Column(Text, nullable=True)
    # latitude = Column(Float, nullable=True)
    # longitude = Column(Float, nullable=True)
    # filesize = Column(Integer, nullable=True)

    # Relationship back to Site (many-to-one)
    site = relationship("Site", back_populates="photos")
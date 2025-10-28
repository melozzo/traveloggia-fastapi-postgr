from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from sqlalchemy import Float


class Photo(Base):
    __tablename__ = "photos"

    photoid = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=True)
    caption = Column(String, nullable=True)
    siteid = Column(Integer, ForeignKey("sites.siteid"), nullable=True, index=True)
    journalid = Column(Integer, nullable=True)
    dateadded = Column(DateTime, nullable=True)
    datetaken = Column(DateTime, nullable=True)
    fromphone = Column(Boolean, nullable=True)
    storageurl = Column(String, nullable=False)
    thumbnailurl = Column(String, nullable=True)
    orientation = Column(String, nullable=True)
    orientationid = Column(Integer, nullable=True)
    gpslatitude = Column('gpslatitude', Float, nullable=True)
    gpslongitude = Column('gpslongitude', Float, nullable=True)
    camera = Column(String, nullable=True)
    model = Column(String, nullable=True)
    software = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    bitspersample = Column(Integer, nullable=True)
    isdeleted = Column(Boolean, nullable=True)

    site = relationship("Site", back_populates="photos")
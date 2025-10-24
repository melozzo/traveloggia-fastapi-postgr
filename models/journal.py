from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Journal(Base):
    __tablename__ = "journals"

    # Primary key
    journalid = Column(Integer, primary_key=True, index=True)

    # Foreign key to Site
    siteid = Column(Integer, ForeignKey("sites.siteid"), nullable=False, index=True)

    # Journal properties
    journaltitle = Column(String(500), nullable=True)
    journaltext = Column(Text, nullable=True)
    journaldate = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)
    isdeleted = Column(Boolean, default=False)

    # Add other Journal columns based on your actual table structure:
    # memberid = Column(Integer, nullable=True)
    # ispublic = Column(Boolean, default=True)
    # tags = Column(String(255), nullable=True)

    # Relationship back to Site (many-to-one)
    site = relationship("Site", back_populates="journals")
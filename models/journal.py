from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Journal(Base):
    __tablename__ = "journal"

    # Primary key
    journalid = Column(Integer, primary_key=True, index=True)

    # Foreign key to Site
    siteid = Column(Integer, ForeignKey("sites.siteid"), nullable=False, index=True)

    # Journal properties
    text = Column(Text, nullable=True)
    keywords = Column(String, nullable=True)
    journaldate = Column(DateTime, nullable=True)
    dateadded = Column(DateTime, nullable=True)
    fromphone = Column(Boolean, nullable=True)
    title = Column(String, nullable=True)
    memberid = Column(Integer, nullable=True)
    isdeleted = Column(Boolean, nullable=True)

    # Add other Journal columns based on your actual table structure:
    # memberid = Column(Integer, nullable=True)
    # ispublic = Column(Boolean, default=True)
    # tags = Column(String(255), nullable=True)

    # Relationship back to Site (many-to-one)
    site = relationship("Site", back_populates="journals")
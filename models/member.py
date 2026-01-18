from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from database import Base

class Member(Base):
    __tablename__ = "members"

    # Adjust these columns based on your actual Members table structure
    memberid = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=True)  # Added for authentication
    firstname = Column(String(100), nullable=True)
    lastname = Column(String(100), nullable=True)
    accountcreatedate = Column(DateTime, nullable=True)

    # Add other columns as needed from your .NET model:
    # createddate = Column(DateTime, nullable=True)
    # isactive = Column(Boolean, default=True)
    # phone = Column(String(20), nullable=True)
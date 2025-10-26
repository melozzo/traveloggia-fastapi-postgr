from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Unhandled(Base):
    __tablename__ = "unhandled"

    recordid = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=True)
    exceptionname = Column(String, nullable=True)
    message = Column(String, nullable=True)
    stacktrace = Column(String, nullable=True)
    data = Column(String, nullable=True)
    innerexception = Column(String, nullable=True)
    phoneid = Column(String, nullable=True)
    os = Column(String, nullable=True)
    model = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    memberid = Column(Integer, nullable=True)

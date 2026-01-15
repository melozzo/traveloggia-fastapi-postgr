from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JournalBase(BaseModel):
    text: Optional[str] = None
    siteid: Optional[int] = None
    keywords: Optional[str] = None
    dateadded: Optional[datetime] = None
    journaldate: Optional[datetime] = None
    fromphone: Optional[bool] = None
    title: Optional[str] = None
    memberid: Optional[int] = None
    isdeleted: Optional[bool] = None

class JournalResponse(JournalBase):
    journalid: int
    
    model_config = {"from_attributes": True}

class JournalCreate(BaseModel):
    siteid: int
    title: Optional[str] = None
    text: Optional[str] = None
    journaldate: Optional[datetime] = None
    keywords: Optional[str] = None
    memberid: Optional[int] = None
    class Config:
        extra = "ignore"

class JournalUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    journaldate: Optional[datetime] = None
    keywords: Optional[str] = None
    isdeleted: Optional[bool] = None
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
    siteid: int
    dateadded: Optional[datetime] = None
    model_config = {"from_attributes": True}

class JournalCreate(BaseModel):
    siteid: int
    journaltitle: Optional[str] = None
    journaltext: Optional[str] = None
    journaldate: Optional[datetime] = None

class JournalUpdate(BaseModel):
    journaltitle: Optional[str] = None
    journaltext: Optional[str] = None
    journaldate: Optional[datetime] = None
    isdeleted: Optional[bool] = None
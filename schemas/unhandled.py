from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UnhandledBase(BaseModel):
    recordid: Optional[int] = None
    date: Optional[datetime] = None
    exceptionname: Optional[str] = None
    message: Optional[str] = None
    stacktrace: Optional[str] = None
    data: Optional[str] = None
    innerexception: Optional[str] = None
    phoneid: Optional[str] = None
    os: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    memberid: Optional[int] = None

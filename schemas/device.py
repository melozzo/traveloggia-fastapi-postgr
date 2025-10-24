from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    devicename: Optional[str] = None
    devicetype: Optional[str] = None
    devicetoken: Optional[str] = None
    memberid: Optional[int] = None

class DeviceResponse(DeviceBase):
    id: int
    daterecorded: Optional[datetime] = None
    model_config = {"from_attributes": True}

class DeviceCreate(BaseModel):
    devicename: Optional[str] = None
    devicetype: Optional[str] = None
    devicetoken: Optional[str] = None
    memberid: Optional[int] = None

class DeviceUpdate(BaseModel):
    devicename: Optional[str] = None
    devicetype: Optional[str] = None
    devicetoken: Optional[str] = None
    memberid: Optional[int] = None
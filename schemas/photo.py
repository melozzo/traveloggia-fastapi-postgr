from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PhotoBase(BaseModel):
    photoname: Optional[str] = None
    photopath: Optional[str] = None
    datetaken: Optional[datetime] = None
    isdeleted: Optional[bool] = False

class PhotoResponse(PhotoBase):
    photoid: int
    siteid: int
    dateadded: Optional[datetime] = None
    model_config = {"from_attributes": True}

class PhotoCreate(BaseModel):
    siteid: int
    photoname: Optional[str] = None
    photopath: Optional[str] = None
    datetaken: Optional[datetime] = None

class PhotoUpdate(BaseModel):
    photoname: Optional[str] = None
    photopath: Optional[str] = None
    datetaken: Optional[datetime] = None
    isdeleted: Optional[bool] = None
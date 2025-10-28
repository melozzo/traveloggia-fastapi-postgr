from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PhotoBase(BaseModel):
    filename: Optional[str] = None
    caption: Optional[str] = None
    siteid: Optional[int] = None
    journalid: Optional[int] = None
    dateadded: Optional[datetime] = None
    datetaken: Optional[datetime] = None
    fromphone: Optional[bool] = None
    storageurl: Optional[str] = None
    thumbnailurl: Optional[str] = None
    orientation: Optional[str] = None
    orientationid: Optional[int] = None
    gpslatitude: Optional[float] = None
    gpslongitude: Optional[float] = None
    camera: Optional[str] = None
    model: Optional[str] = None
    software: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    bitspersample: Optional[int] = None
    isdeleted: Optional[bool] = None

class PhotoResponse(PhotoBase):
    photoid: int
    siteid: int
    dateadded: Optional[datetime] = None
    model_config = {"from_attributes": True}

class PhotoCreate(PhotoBase):
    siteid: int

class PhotoUpdate(BaseModel):
    photoname: Optional[str] = None
    photopath: Optional[str] = None
    datetaken: Optional[datetime] = None
    isdeleted: Optional[bool] = None
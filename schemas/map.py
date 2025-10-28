from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from schemas.site import SiteResponse





class MapBase(BaseModel):
    mapname: Optional[str] = None
    memberid: int
    crowdsourced: Optional[bool] = False
    fromphone: Optional[bool] = False
    haslayers: Optional[bool] = False
    isdeleted: Optional[bool] = False

class MapResponse(MapBase):
    mapid: int
    createdate: Optional[datetime] = None
    lastrevision: Optional[datetime] = None
    Sites: List[SiteResponse] = []  # Include related sites
    model_config = {"from_attributes": True}

class MapListItem(BaseModel):
    mapid: int
    mapname: Optional[str] = None
    memberid: int
    createdate: Optional[datetime] = None
    model_config = {"from_attributes": True}

class MapCreate(BaseModel):
    mapname: Optional[str] = None
    memberid: int
    crowdsourced: Optional[bool] = False
    fromphone: Optional[bool] = False
    haslayers: Optional[bool] = False
    class Config:
        extra = "ignore"

class MapUpdate(BaseModel):
    mapname: Optional[str] = None
    crowdsourced: Optional[bool] = None
    fromphone: Optional[bool] = None
    haslayers: Optional[bool] = None
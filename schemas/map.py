from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SiteBase(BaseModel):
    sitename: Optional[str] = None
    routeindex: Optional[int] = None
    arrival: Optional[datetime] = None
    isdeleted: Optional[bool] = False

class SiteResponse(SiteBase):
    siteid: int
    mapid: int
    dateadded: Optional[datetime] = None
    model_config = {"from_attributes": True}

class SiteCreate(BaseModel):
    mapid: int
    sitename: Optional[str] = None
    routeindex: Optional[int] = None
    arrival: Optional[datetime] = None

class SiteUpdate(BaseModel):
    sitename: Optional[str] = None
    routeindex: Optional[int] = None
    arrival: Optional[datetime] = None
    isdeleted: Optional[bool] = None

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
    sites: List[SiteResponse] = []  # Include related sites
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

class MapUpdate(BaseModel):
    mapname: Optional[str] = None
    crowdsourced: Optional[bool] = None
    fromphone: Optional[bool] = None
    haslayers: Optional[bool] = None
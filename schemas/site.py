from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SiteBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    url: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    dateadded: Optional[datetime] = None
    fromphone: Optional[bool] = None
    rating: Optional[int] = None
    averagerating: Optional[float] = None
    votescast: Optional[int] = None
    routeindex: Optional[int] = None
    arrival: Optional[datetime] = None
    departure: Optional[datetime] = None
    memberid: Optional[int] = None
    isdeleted: Optional[bool] = None

class SiteResponse(SiteBase):
    siteid: int
    mapid: int
    model_config = {"from_attributes": True}

class SiteCreate(SiteBase):
    mapid: int

class SiteUpdate(SiteBase):
    pass

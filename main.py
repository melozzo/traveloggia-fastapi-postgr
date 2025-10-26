from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine
from models.member import Member
from models.map import Map
from models.site import Site
from models.photo import Photo
from models.journal import Journal
from models.device import Device
from schemas.member import MemberRequest, MemberResponse, LoginRequest
from schemas.map import MapResponse, MapListItem, MapCreate, MapUpdate
from schemas.site import SiteResponse, SiteCreate, SiteUpdate
from schemas.photo import PhotoResponse, PhotoCreate, PhotoUpdate
from schemas.journal import JournalResponse, JournalCreate, JournalUpdate
from schemas.device import DeviceResponse, DeviceCreate, DeviceUpdate
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

import models
from routers.member import router as member_router
from routers.map import router as map_router
from routers.device import router as device_router
from routers.journal import router as journal_router
from routers.photo import router as photo_router
from routers.site import router as site_router


app = FastAPI(title="Traveloggia API", version="1.0.0")

# Response schemas for Swagger documentation
class RootResponse(BaseModel):
    message: str
    status: str

class HealthResponse(BaseModel):
    status: str
    database: Optional[str] = None
    error: Optional[str] = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables (if they don't exist)
# models.Base.metadata.create_all(bind=engine)


@app.get("/", response_model=RootResponse)
async def root():
    """Root endpoint - returns server status"""
    return {"message": "Traveloggia FastAPI Server", "status": "running"}


# Include routers
app.include_router(member_router)
app.include_router(map_router)
app.include_router(device_router)
app.include_router(journal_router)
app.include_router(photo_router)
app.include_router(site_router)



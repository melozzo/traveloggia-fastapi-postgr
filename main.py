from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine
from models.member import Member
from models.map import Map, Site
from models.photo import Photo
from models.journal import Journal
from models.device import Device
from schemas.member import MemberRequest, MemberResponse, LoginRequest
from schemas.map import MapResponse, MapListItem, MapCreate, MapUpdate, SiteResponse, SiteCreate, SiteUpdate
from schemas.photo import PhotoResponse, PhotoCreate, PhotoUpdate
from schemas.journal import JournalResponse, JournalCreate, JournalUpdate
from schemas.device import DeviceResponse, DeviceCreate, DeviceUpdate
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import models

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

from pydantic import BaseModel

@app.get("/", response_model=RootResponse)
async def root():
    """Root endpoint - returns server status"""
    return {"message": "Traveloggia FastAPI Server", "status": "running"}



from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import get_db
from models.map import Map  # adjust import as needed
from schemas.map import MapListItem  # adjust import as needed

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://www.traveloggia.pro",
        "https://www.traveloggia.pro",
        "https://traveloggia.pro",
        "http://traveloggia.pro",
        "http://127.0.0.1:3000",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/MapList/{id}", response_model=list[MapListItem])
async def get_map_list(id: int, db: Session = Depends(get_db)):
    """
    GET: api/MapList/5 - Get list of maps for member
    """
    maps = db.query(Map).filter(
        Map.memberid == id,
        Map.isdeleted != True
    ).order_by(Map.createdate.desc()).all()
    return [MapListItem.model_validate(m) for m in maps]


@app.post("/api/Members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(member_req: MemberRequest, db: Session = Depends(get_db)):
    """Create a new member. If a member with the same email exists, return 400."""
    existing = db.query(Member).filter(Member.email == member_req.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member with that email already exists")
    new_member = Member(email=member_req.email, firstname=getattr(member_req, 'firstname', None), lastname=getattr(member_req, 'lastname', None))
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@app.get("/api/Members/{id}", response_model=MemberResponse)
async def get_member(id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.memberid == id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member
# NOTE: members list endpoint temporarily disabled to avoid exposing full dataset
# @app.get("/api/Members", response_model=list[MemberResponse])
# async def list_members(limit: int = 100, db: Session = Depends(get_db)):
#     """Return a list of members (limited to `limit` rows)."""
#     members = db.query(Member).order_by(Member.Id).limit(limit).all()
#     return [MemberResponse.from_attributes(m) if hasattr(MemberResponse, 'from_attributes') else m for m in members]

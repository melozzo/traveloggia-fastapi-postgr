
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models.member import Member
from schemas.member import MemberRequest, MemberResponse, LoginRequest
from datetime import datetime
from models.map import Map

router = APIRouter()

# ValidateMember endpoint: POST /api/Members/validate
@router.post("/api/Members/validate", response_model=MemberResponse)
async def validate_member(login: LoginRequest, db: Session = Depends(get_db)):
    # FastAPI handles CORS globally, so no need to set headers here
    member = db.query(Member).filter(Member.email == login.email).first()
    if not member or member.password != login.password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password")
    return member




# Delete member endpoint
@router.delete("/api/Members/{id}", response_model=MemberResponse)
async def delete_member(id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.memberid == id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    db.delete(member)
    db.commit()
    return member



# Create member and default map endpoint
@router.post("/api/Members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def post_member(member_req: MemberRequest, db: Session = Depends(get_db)):
    # Check if member already exists
    member_already = db.query(Member).filter(Member.email == member_req.email).first()
    if member_already:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member exists already")
    # Create new member
    new_member = Member(
        email=member_req.email,
        firstname=getattr(member_req, 'firstname', None),
        lastname=getattr(member_req, 'lastname', None),
        accountcreatedate=datetime.now()
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    # Create default map for new member
    default_map = Map(
        memberid=new_member.memberid,
        createdate=datetime.now(),
        mapname=f"DefaultMap {datetime.now().date()}"
    )
    try:
        db.add(default_map)
        db.commit()
    except Exception:
        pass
    return new_member


@router.post("/api/Members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(member_req: MemberRequest, db: Session = Depends(get_db)):
    existing = db.query(Member).filter(Member.email == member_req.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member with that email already exists")
    new_member = Member(email=member_req.email, firstname=getattr(member_req, 'firstname', None), lastname=getattr(member_req, 'lastname', None))
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.get("/api/Members/{id}", response_model=MemberResponse)
async def get_member(id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.memberid == id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member

@router.post("/api/Members", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member(member_req: MemberRequest, db: Session = Depends(get_db)):
    existing = db.query(Member).filter(Member.email == member_req.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member with that email already exists")
    new_member = Member(email=member_req.email, firstname=getattr(member_req, 'firstname', None), lastname=getattr(member_req, 'lastname', None))
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


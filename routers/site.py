from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.site import Site
from schemas.site import SiteResponse, SiteCreate, SiteUpdate

router = APIRouter()

# GET: SelectSite by ID
@router.get("/api/SelectSite/{id}", response_model=SiteResponse)
async def select_site(id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.siteid == id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return SiteResponse.model_validate(site, from_attributes=True)

# POST: Create new site
@router.post("/api/Sites", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_site(site_create: SiteCreate, db: Session = Depends(get_db)):
    new_site = Site(**site_create.model_dump())
    new_site.dateadded = new_site.dateadded or None
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return SiteResponse.model_validate(new_site, from_attributes=True)

# PUT: Update a site
@router.put("/api/Sites/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_site(id: int, site_update: SiteUpdate, db: Session = Depends(get_db)):
    site_obj = db.query(Site).filter(Site.siteid == id).first()
    if not site_obj:
        raise HTTPException(status_code=404, detail="Site not found")
    # Update fields
    for field, value in site_update.model_dump(exclude_unset=True).items():
        setattr(site_obj, field, value)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating site")
    return

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.site import Site
from schemas.map import SiteResponse

router = APIRouter()

# Example endpoint for sites
@router.get("/api/Sites/{id}", response_model=SiteResponse)
async def get_site(id: int, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.siteid == id).first()
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site not found")
    return site

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.photo import Photo
from schemas.photo import PhotoCreate, PhotoResponse

router = APIRouter()

# Example endpoint for photos
@router.get("/api/Photos/{id}", response_model=PhotoResponse)
async def get_photo(id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.siteid == id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    return photo

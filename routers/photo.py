from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.photo import Photo
from schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate

router = APIRouter()

# Example endpoint for photos

# GET: api/Photos/{id} - get all photos for a site
from typing import List
@router.get("/api/Photos/{id}", response_model=List[PhotoResponse])
async def get_photos(id: int, db: Session = Depends(get_db)):
    photos = db.query(Photo).filter(Photo.siteid == id).all()
    return [PhotoResponse.model_validate(photo, from_attributes=True) for photo in photos]

# GET: api/Photo/{id} - get a single photo by id
@router.get("/api/Photo/{id}", response_model=PhotoResponse)
async def get_photo(id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.photoid == id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return PhotoResponse.model_validate(photo, from_attributes=True)


# POST: api/Photos - create a new photo with debugging
@router.post("/api/Photos", response_model=PhotoResponse)
async def post_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    import logging
    from datetime import datetime
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info(f"Received photo data: {photo}")
        new_photo = Photo(**photo.model_dump())
        new_photo.dateadded = datetime.now()
        if new_photo.datetaken:
            logging.info(f"datetaken before conversion: {new_photo.datetaken}")
            try:
                new_photo.datetaken = new_photo.datetaken.astimezone()
            except Exception as e:
                logging.error(f"Error converting datetaken timezone: {e}")
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)
        logging.info(f"Photo created with ID: {new_photo.photoid}")
        return PhotoResponse.model_validate(new_photo, from_attributes=True)
    except Exception as e:
        logging.error(f"Error in photo creation: {e}")
        raise HTTPException(status_code=400, detail=f"Photo creation failed: {e}")

# PUT: api/Photos/{id} - update a photo
@router.put("/api/Photos/{id}", response_model=None)
async def put_photo(id: int, photo: PhotoUpdate, db: Session = Depends(get_db)):
    db_photo = db.query(Photo).filter(Photo.photoid == id).first()
    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    for key, value in photo.model_dump(exclude_unset=True).items():
        setattr(db_photo, key, value)
    db.commit()
    return

# DELETE: api/Photos/{id} - delete a photo
@router.delete("/api/Photos/{id}", response_model=PhotoResponse)
async def delete_photo(id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.photoid == id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.delete(photo)
    db.commit()
    return PhotoResponse.model_validate(photo, from_attributes=True)
